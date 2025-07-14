"""
Enhanced Shift Assignment Algorithm
改良された自動シフト割当エンジン
"""

import math
import random
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from django.db import models
from django.db.models import Count, Q
from typing import List, Dict, Tuple, Optional


class ShiftAssignmentRule(models.Model):
    """シフト割当ルール"""

    name = models.CharField(max_length=100, verbose_name="ルール名")

    # 連続勤務制限
    max_consecutive_days = models.IntegerField(
        default=5, verbose_name="最大連続勤務日数"
    )
    min_rest_days = models.IntegerField(default=1, verbose_name="最小休日数")
    max_night_shifts_per_week = models.IntegerField(
        default=2, verbose_name="週最大夜勤回数"
    )

    # 公平性重み
    priority_weight = models.DecimalField(
        max_digits=3, decimal_places=2, default=1.0, verbose_name="希望優先度重み"
    )
    experience_weight = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.3, verbose_name="経験値重み"
    )
    workload_balance_weight = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.8, verbose_name="負荷均等重み"
    )

    # その他制約
    allow_preference_override = models.BooleanField(
        default=False, verbose_name="希望無視許可"
    )
    enforce_position_requirements = models.BooleanField(
        default=True, verbose_name="職種要件強制"
    )

    is_active = models.BooleanField(default=True, verbose_name="有効")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "シフト割当ルール"
        verbose_name_plural = "シフト割当ルール"

    def __str__(self):
        return self.name


class EnhancedShiftAssignmentEngine:
    """改良シフト割当エンジン"""

    def __init__(self, assignment_rule: Optional[ShiftAssignmentRule] = None):
        self.rule = (
            assignment_rule
            or ShiftAssignmentRule.objects.filter(is_active=True).first()
        )
        self.assignment_score_cache = {}

    def assign_shifts_for_period(
        self, start_date: datetime, end_date: datetime
    ) -> Dict:
        """期間内のシフト自動割当"""
        from shifts.models import Employee, ShiftRequest, ShiftRequirement, Shift

        results = {
            "assigned_shifts": [],
            "unassigned_requests": [],
            "conflicts": [],
            "statistics": {},
        }

        # 1. データ準備
        employees = self._get_available_employees()
        requests = self._get_shift_requests(start_date, end_date)
        requirements = self._get_shift_requirements()
        existing_shifts = self._get_existing_shifts(start_date, end_date)

        # 2. 従業員の勤務履歴分析
        employee_stats = self._analyze_employee_workload(employees, start_date)

        # 3. 日別・職種別割当処理
        current_date = start_date.date()
        while current_date <= end_date.date():
            day_name = current_date.strftime("%A")
            daily_requirements = requirements.get(day_name, {})

            if daily_requirements:
                day_result = self._assign_daily_shifts(
                    current_date,
                    daily_requirements,
                    requests,
                    employees,
                    employee_stats,
                    existing_shifts,
                )
                results["assigned_shifts"].extend(day_result["assigned"])
                results["unassigned_requests"].extend(day_result["unassigned"])
                results["conflicts"].extend(day_result["conflicts"])

            current_date += timedelta(days=1)

        # 4. 統計情報計算
        results["statistics"] = self._calculate_assignment_statistics(results)

        return results

    def _assign_daily_shifts(
        self,
        date,
        requirements,
        all_requests,
        employees,
        employee_stats,
        existing_shifts,
    ):
        """1日分のシフト割当"""
        result = {"assigned": [], "unassigned": [], "conflicts": []}

        # その日の希望を取得
        daily_requests = [r for r in all_requests if r.requested_date == date]

        # 職種別に処理
        for position, required_count in requirements.items():
            position_requests = [
                r for r in daily_requests if r.employee.position == position
            ]

            # スコア計算して優先順位決定
            scored_requests = []
            for request in position_requests:
                score = self._calculate_assignment_score(
                    request, date, employee_stats, existing_shifts
                )
                scored_requests.append((score, request))

            # スコア降順でソート
            scored_requests.sort(key=lambda x: x[0], reverse=True)

            # 上位から割当
            assigned_count = 0
            for score, request in scored_requests:
                if assigned_count >= required_count:
                    result["unassigned"].append(request)
                    continue

                # 制約チェック
                if self._check_assignment_constraints(request, date, existing_shifts):
                    result["assigned"].append(
                        {"request": request, "score": score, "assigned_date": date}
                    )
                    # 既存シフトに追加（次の制約チェック用）
                    existing_shifts.append(
                        {
                            "employee_id": request.employee.id,
                            "date": date,
                            "shift_type": request.shift_type,
                        }
                    )
                    assigned_count += 1
                else:
                    result["conflicts"].append(
                        {"request": request, "reason": "制約違反", "date": date}
                    )

        return result

    def _calculate_assignment_score(
        self, request, date, employee_stats, existing_shifts
    ) -> float:
        """割当スコア計算"""
        cache_key = f"{request.employee.id}_{date}_{request.shift_type}"
        if cache_key in self.assignment_score_cache:
            return self.assignment_score_cache[cache_key]

        score = 0.0

        # 1. 希望優先度スコア
        priority_score = request.priority * float(self.rule.priority_weight)
        score += priority_score

        # 2. 経験値スコア
        experience_score = self._calculate_experience_score(
            request.employee, request.shift_type
        )
        score += experience_score * float(self.rule.experience_weight)

        # 3. 負荷均等スコア
        workload_score = self._calculate_workload_balance_score(
            request.employee.id, date, employee_stats
        )
        score += workload_score * float(self.rule.workload_balance_weight)

        # 4. 連続勤務ペナルティ
        consecutive_penalty = self._calculate_consecutive_penalty(
            request.employee.id, date, existing_shifts
        )
        score -= consecutive_penalty

        # 5. 夜勤頻度調整
        if self._is_night_shift(request.shift_type):
            night_penalty = self._calculate_night_shift_penalty(
                request.employee.id, date, existing_shifts
            )
            score -= night_penalty

        self.assignment_score_cache[cache_key] = score
        return score

    def _calculate_experience_score(self, employee, shift_type) -> float:
        """経験値スコア計算"""
        # 過去の同シフト勤務回数を考慮
        from shifts.models import Shift

        past_shifts = Shift.objects.filter(
            employee=employee,
            shift_type=shift_type,
            created_at__gte=datetime.now() - timedelta(days=90),
        ).count()

        # 経験豊富ほど高スコア（但し上限設定）
        return min(past_shifts * 0.1, 1.0)

    def _calculate_workload_balance_score(
        self, employee_id, date, employee_stats
    ) -> float:
        """負荷均等スコア計算"""
        stats = employee_stats.get(employee_id, {})

        # 今月の勤務日数が少ないほど高スコア
        monthly_days = stats.get("monthly_days", 0)
        max_monthly_days = max(
            [s.get("monthly_days", 0) for s in employee_stats.values()] + [1]
        )

        balance_ratio = 1.0 - (monthly_days / max_monthly_days)
        return balance_ratio * 2.0  # 最大2.0点

    def _calculate_consecutive_penalty(
        self, employee_id, date, existing_shifts
    ) -> float:
        """連続勤務ペナルティ計算"""
        consecutive_days = self._count_consecutive_days(
            employee_id, date, existing_shifts
        )

        if consecutive_days >= self.rule.max_consecutive_days:
            return 10.0  # 大幅ペナルティ
        elif consecutive_days >= (self.rule.max_consecutive_days - 1):
            return 5.0  # 中程度ペナルティ

        return 0.0

    def _calculate_night_shift_penalty(
        self, employee_id, date, existing_shifts
    ) -> float:
        """夜勤頻度ペナルティ計算"""
        week_start = date - timedelta(days=date.weekday())
        week_night_shifts = sum(
            1
            for shift in existing_shifts
            if (
                shift["employee_id"] == employee_id
                and week_start <= shift["date"] <= date
                and self._is_night_shift(shift["shift_type"])
            )
        )

        if week_night_shifts >= self.rule.max_night_shifts_per_week:
            return 8.0

        return 0.0

    def _check_assignment_constraints(self, request, date, existing_shifts) -> bool:
        """割当制約チェック"""
        employee_id = request.employee.id

        # 連続勤務日数チェック
        consecutive_days = self._count_consecutive_days(
            employee_id, date, existing_shifts
        )
        if consecutive_days >= self.rule.max_consecutive_days:
            return False

        # 夜勤頻度チェック
        if self._is_night_shift(request.shift_type):
            week_start = date - timedelta(days=date.weekday())
            week_night_shifts = sum(
                1
                for shift in existing_shifts
                if (
                    shift["employee_id"] == employee_id
                    and week_start <= shift["date"] <= date
                    and self._is_night_shift(shift["shift_type"])
                )
            )
            if week_night_shifts >= self.rule.max_night_shifts_per_week:
                return False

        # 同日重複チェック
        same_day_shifts = [
            s
            for s in existing_shifts
            if s["employee_id"] == employee_id and s["date"] == date
        ]
        if same_day_shifts:
            return False

        return True

    def _count_consecutive_days(self, employee_id, date, existing_shifts) -> int:
        """連続勤務日数カウント"""
        consecutive = 0
        check_date = date - timedelta(days=1)

        while True:
            day_shifts = [
                s
                for s in existing_shifts
                if s["employee_id"] == employee_id and s["date"] == check_date
            ]
            if not day_shifts:
                break
            consecutive += 1
            check_date -= timedelta(days=1)

        return consecutive

    def _is_night_shift(self, shift_type) -> bool:
        """夜勤判定"""
        # shift_typeが文字列の場合とオブジェクトの場合に対応
        if hasattr(shift_type, "is_night_shift"):
            return shift_type.is_night_shift
        return "night" in str(shift_type).lower() or "夜勤" in str(shift_type)

    def _get_available_employees(self):
        """利用可能従業員取得"""
        from shifts.models import Employee

        return Employee.objects.filter(is_active=True)

    def _get_shift_requests(self, start_date, end_date):
        """シフト希望取得"""
        from shifts.models import ShiftRequest

        return ShiftRequest.objects.filter(
            requested_date__range=[start_date.date(), end_date.date()], approved=True
        ).select_related("employee")

    def _get_shift_requirements(self):
        """シフト必要人数取得"""
        from shifts.models import ShiftRequirement

        requirements = {}
        for req in ShiftRequirement.objects.all():
            requirements[req.day_of_week] = {
                "看護師": req.nurse_required,
                "臨床工学技士": req.engineer_required,
                "介護福祉士": req.assistant_required,
            }
        return requirements

    def _get_existing_shifts(self, start_date, end_date):
        """既存シフト取得"""
        from shifts.models import Shift

        shifts = []
        for shift in Shift.objects.filter(
            shift_date__range=[start_date.date(), end_date.date()]
        ).select_related("employee", "shift_type"):
            shifts.append(
                {
                    "employee_id": shift.employee.id,
                    "date": shift.shift_date,
                    "shift_type": shift.shift_type,
                }
            )
        return shifts

    def _analyze_employee_workload(self, employees, start_date):
        """従業員勤務負荷分析"""
        from shifts.models import Shift

        stats = {}

        for employee in employees:
            monthly_shifts = Shift.objects.filter(
                employee=employee,
                shift_date__month=start_date.month,
                shift_date__year=start_date.year,
            ).count()

            stats[employee.id] = {
                "monthly_days": monthly_shifts,
                "weekly_average": monthly_shifts / 4.0,
                "last_shift_date": None,  # 実装は省略
            }

        return stats

    def _calculate_assignment_statistics(self, results):
        """割当統計計算"""
        total_requests = len(results["assigned_shifts"]) + len(
            results["unassigned_requests"]
        )
        assigned_count = len(results["assigned_shifts"])

        return {
            "total_requests": total_requests,
            "assigned_count": assigned_count,
            "assignment_rate": (assigned_count / total_requests * 100)
            if total_requests > 0
            else 0,
            "conflicts_count": len(results["conflicts"]),
        }
