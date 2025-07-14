"""
Optimized views with performance improvements
N+1クエリ問題の解決とチャンク処理実装
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator
import csv
import io
from datetime import datetime, timedelta

from shifts.models import Shift, Employee, ShiftRequest


@login_required
def shift_list_optimized(request):
    """N+1クエリ問題を解決したシフト一覧"""
    shifts = (
        Shift.objects.select_related(
            "employee__user", "shift_type", "requested_by", "approved_by"
        )
        .prefetch_related("employee__department", "attendance")
        .filter(shift_date__gte=datetime.now().date() - timedelta(days=30))
        .order_by("-shift_date", "employee__name")
    )

    # ページネーション実装
    paginator = Paginator(shifts, 50)  # 50件ずつ表示
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "shifts/shift_list_optimized.html",
        {"page_obj": page_obj, "total_shifts": paginator.count},
    )


@login_required
def employee_csv_import_chunked(request):
    """チャンク処理による大容量CSVインポート"""
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]

        try:
            # メモリ効率的な処理
            file_data = csv_file.read().decode("utf-8")
            csv_reader = csv.DictReader(io.StringIO(file_data))

            # チャンクサイズ設定
            CHUNK_SIZE = 100
            employees_batch = []
            processed_count = 0
            error_count = 0

            with transaction.atomic():
                for row in csv_reader:
                    try:
                        # バリデーション
                        if not row.get("name") or not row.get("email"):
                            error_count += 1
                            continue

                        # Employee オブジェクト作成（まだ保存しない）
                        employee = Employee(
                            name=row["name"].strip(),
                            email=row["email"].strip(),
                            department=row.get("department", "").strip(),
                            position=row.get("position", "").strip(),
                            phone=row.get("phone", "").strip(),
                        )

                        employees_batch.append(employee)

                        # チャンクサイズに達したらバッチ保存
                        if len(employees_batch) >= CHUNK_SIZE:
                            Employee.objects.bulk_create(
                                employees_batch, ignore_conflicts=True
                            )
                            processed_count += len(employees_batch)
                            employees_batch = []

                    except Exception as e:
                        error_count += 1
                        print(f"行処理エラー: {e}")

                # 残りのデータを保存
                if employees_batch:
                    Employee.objects.bulk_create(employees_batch, ignore_conflicts=True)
                    processed_count += len(employees_batch)

            return JsonResponse(
                {
                    "status": "success",
                    "processed": processed_count,
                    "errors": error_count,
                    "message": f"{processed_count}件の従業員を登録しました（エラー: {error_count}件）",
                }
            )

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": f"インポートエラー: {str(e)}"},
                status=400,
            )

    return render(request, "shifts/csv_import_chunked.html")


@login_required
def dashboard_optimized(request):
    """最適化されたダッシュボード"""
    # 集約クエリでデータベースアクセス最小化
    from django.db.models import Count, Q

    stats = {
        "total_employees": Employee.objects.filter(is_active=True).count(),
        "pending_requests": ShiftRequest.objects.filter(status="pending").count(),
        "shifts_this_month": Shift.objects.filter(
            shift_date__year=datetime.now().year, shift_date__month=datetime.now().month
        ).count(),
        "night_shifts_this_week": Shift.objects.filter(
            shift_date__week=datetime.now().isocalendar()[1],
            shift_type__is_night_shift=True,
        ).count(),
    }

    # 最近のアクティビティ（limit使用）
    recent_shifts = Shift.objects.select_related("employee", "shift_type").order_by(
        "-created_at"
    )[:10]

    return render(
        request,
        "shifts/dashboard_optimized.html",
        {"stats": stats, "recent_shifts": recent_shifts},
    )


def bulk_shift_update(request):
    """一括シフト更新API"""
    if request.method == "POST":
        shift_updates = request.POST.getlist("shift_updates")

        with transaction.atomic():
            for update_data in shift_updates:
                shift_id, new_status = update_data.split(":")
                Shift.objects.filter(id=shift_id).update(status=new_status)

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"}, status=400)
