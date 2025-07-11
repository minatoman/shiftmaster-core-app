# shifts/views/upload_views.py

import os
import io
import csv
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from ..models import Shift, Employee, HolidayRequest
from ..utils import normalize_name

# 🔐 管理者限定ビュー
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

# ✅ 勤務シフトCSVアップロード処理（管理者のみ）
@staff_required
@csrf_exempt
def upload_shifts_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(decoded_file))

            Shift.objects.all().delete()
            success_count = 0
            error_logs = []

            for row in reader:
                name = normalize_name(row.get('氏名', ''))
                raw_date = row.get('日付', '').strip()
                shift_type = row.get('勤務区分')
                location = row.get('配置先') or ""
                notes = row.get('備考') or ""

                if not name:
                    error_logs.append({'氏名': name, '日付': raw_date, 'エラー内容': '氏名が空です'})
                    continue

                shift_date = None
                for fmt in ['%Y/%m/%d', '%Y-%m-%d']:
                    try:
                        shift_date = datetime.strptime(raw_date, fmt).date()
                        break
                    except ValueError:
                        continue

                if not shift_date:
                    error_logs.append({'氏名': name, '日付': raw_date, 'エラー内容': '日付形式エラー'})
                    continue

                try:
                    employee = Employee.objects.get(name=name)
                    Shift.objects.create(
                        employee=employee,
                        shift_date=shift_date,
                        shift_type=shift_type,
                        location=location,
                        notes=notes,
                        is_approved=True
                    )
                    success_count += 1
                except Employee.DoesNotExist:
                    error_logs.append({'氏名': name, '日付': raw_date, 'エラー内容': '該当職員がいません'})
                except Exception as e:
                    error_logs.append({'氏名': name, '日付': raw_date, 'エラー内容': str(e)})

            total = success_count + len(error_logs)
            messages.success(request, f"アップロード完了：成功 {success_count} 件 / エラー {len(error_logs)} 件 / 合計 {total} 件")

            if error_logs:
                export_dir = os.path.join(settings.BASE_DIR, 'shifts', 'temp_exports')
                os.makedirs(export_dir, exist_ok=True)
                file_name = f'error_log_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
                error_log_path = os.path.join(export_dir, file_name)

                with open(error_log_path, 'w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['氏名', '日付', 'エラー内容'])
                    writer.writeheader()
                    writer.writerows(error_logs)

                request.session['error_log_file'] = file_name
                messages.warning(request, "一部エラーがありました。エラーログをダウンロードしてください。")

            return redirect('shift_list')

        except Exception as e:
            messages.error(request, f"CSV読み込みエラー: {e}")
            return redirect('shift_list')

    return render(request, 'shifts/upload_shifts_csv.html')

# ✅ エラーログCSVダウンロード処理
@staff_required
def download_error_log_csv(request):
    file_name = request.GET.get('file') or request.session.get('error_log_file')
    if not file_name:
        messages.error(request, "エラーログファイルが見つかりません。")
        return redirect('shift_list')

    file_path = os.path.join(settings.BASE_DIR, 'shifts', 'temp_exports', file_name)
    if not os.path.exists(file_path):
        messages.error(request, "一時ファイルが削除されています。")
        return redirect('shift_list')

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

# ✅ 職員CSVアップロード（管理者のみ）
@staff_required
@csrf_exempt
def upload_employee_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(decoded_file))

            created, updated, errors = 0, 0, []

            for row in reader:
                name = normalize_name(row.get('氏名', ''))
                if not name:
                    errors.append({'氏名': name, 'エラー内容': '氏名が空です'})
                    continue

                defaults = {
                    'position': row.get('職種', ''),
                    'license': row.get('資格', ''),
                    'department': row.get('所属', ''),
                    'work_details': row.get('業務内容', ''),
                    'committees': row.get('委員会', ''),
                    'evaluation': row.get('評価', ''),
                }

                try:
                    employee, created_flag = Employee.objects.update_or_create(
                        name=name,
                        defaults=defaults
                    )
                    if created_flag:
                        created += 1
                    else:
                        updated += 1
                except Exception as e:
                    errors.append({'氏名': name, 'エラー内容': str(e)})

            total = created + updated + len(errors)
            messages.success(request, f"登録完了：新規 {created} 件 / 更新 {updated} 件 / エラー {len(errors)} 件 / 合計 {total} 件")

            if errors:
                export_dir = os.path.join(settings.BASE_DIR, 'shifts', 'temp_exports')
                os.makedirs(export_dir, exist_ok=True)
                error_log_path = os.path.join(export_dir, f'employee_error_log_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv')

                with open(error_log_path, 'w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['氏名', 'エラー内容'])
                    writer.writeheader()
                    writer.writerows(errors)

                request.session['error_log_file'] = os.path.basename(error_log_path)
                messages.warning(request, "エラーログをダウンロードしてください。")

            return redirect('employee_list')

        except Exception as e:
            messages.error(request, f"CSV処理エラー: {e}")
            return redirect('employee_list')

    return render(request, 'shifts/upload_employee_csv.html')


# ✅ 勤務希望・休暇希望の一括インポート（仮実装）
@staff_required
def import_holiday_requests_csv(request):
    messages.info(request, "📥 import_holiday_requests_csv は現在準備中です（仮のビューです）")
    return redirect('dashboard')


# ✅ 勤務希望・休暇希望のエクスポート（仮実装）
@staff_required
def export_holiday_requests_csv(request):
    messages.info(request, "📤 export_holiday_requests_csv は現在準備中です（仮のビューです）")
    return redirect('dashboard')


# ✅ JSON/CSV一括アップロード用 fixture 仮ビュー
@staff_required
def upload_fixture(request):
    messages.info(request, "📦 upload_fixture は現在準備中です（仮のビューです）")
    return redirect('dashboard')

