# shifts/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    # 🌐 ホーム & 認証
    path('', views.homepage, name='homepage'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),

    # 📋 シフト管理
    path('shifts/', views.shift_list, name='shift_list'),
    path('shifts/add/', views.add_shift, name='add_shift'),
    path('shifts/edit/<int:shift_id>/', views.edit_shift, name='edit_shift'),
    path('shifts/delete/<int:shift_id>/', views.delete_shift, name='delete_shift'),
    path('shifts/confirm_delete/<int:shift_id>/', views.confirm_delete_shift, name='confirm_delete_shift'),
    path('shifts/approve/<int:shift_id>/', views.approve_shift, name='approve_shift'),
    path('shifts/register/', views.add_shift, name='shift_register'),  # ✅ テスト互換のために明示定義

    # 🙋‍♀️ 勤務希望・休暇申請
    path('shifts/requests/', views.shift_request_list, name='shift_request_list'),
    path('shifts/holidays/add/', views.add_holiday_request, name='add_holiday_request'),

    # 🤖 自動割当（AI風）
    path('shifts/auto_assign/', views.auto_assign, name='auto_assign'),

    # 📤 勤務希望データ 出力・入力（CSV / Excel / PDF）
    path('shifts/requests/export/csv/', views.export_shift_requests_csv, name='export_shift_requests_csv'),
    path('shifts/requests/export/excel/', views.export_shift_requests_excel, name='export_shift_requests_excel'),
    path('shifts/requests/import/csv/', views.import_shift_requests_csv, name='import_shift_requests_csv'),
    path('shifts/requests/import/excel/', views.import_shift_requests_excel, name='import_shift_requests_excel'),
    path('shifts/export/pdf/', views.export_shift_pdf, name='export_shift_pdf'),

    # ✅ シフトCSVアップロード（管理者専用・上書き登録）
    path('shifts/upload_csv/', views.upload_shifts_csv, name='upload_shifts_csv'),
    path('shifts/error_log/download/', views.download_error_log_csv, name='download_error_log_csv'),

    # 📅 カレンダー & 統計
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/events/', views.calendar_event_api, name='calendar_event_api'),
    path('summary/monthly/', views.monthly_shift_summary, name='monthly_shift_summary'),
    path('dashboard/chart/json/', views.dashboard_chart_json, name='dashboard_chart_json'),  # ✅ 修正対象

    # 📩 AJAX JSON API（勤務希望追加用）
    path('api/shift_request/', views.shift_request_api, name='shift_request_api'),

    # 💉 透析日誌 関連
    path('dialysis/', views.dialysis_daily_view, name='dialysis_daily'),
    path('dialysis/<str:selected_date>/', views.dialysis_daily_view, name='dialysis_daily_date'),
    path('dialysis/register/', views.dialysis_register_view, name='dialysis_register'),
    path('dialysis/import/', views.import_dialysis_csv, name='import_dialysis_csv'),  # ✅ 修正対象
    path('dialysis/export/pdf/<str:date_str>/', views.dialysis_pdf_export, name='dialysis_pdf_export'),  # ✅ 修正対象
    path('dialysis/calendar/', views.dialysis_calendar_api_events, name='dialysis_calendar_api'),

    # 📄 テンプレート3ブロック（Bootstrap対応）
    path('shifts/template/3block/', views.view_generated_shift_template, name='shift_template_3block'),
    path('templates/', views.template_links_view, name='template_links'),

    # 🧭 管理ダッシュボード（リンク一覧）
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 🧭 スタッフ管理（一覧・登録・編集・重複削除）
    path('staff/', views.employee_list, name='employee_list'),
    path('staff/add/', views.employee_create, name='employee_create'),
    path('staff/upload/', views.upload_employee_csv, name='upload_employee_csv'),
    path('staff/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('staff/detail/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('staff/delete_duplicates/', views.delete_duplicates, name='delete_duplicates'),
    path('staff/upload_fixture/', views.upload_fixture, name='upload_fixture'),

    # 🗂️ 勤務希望・休暇希望（CSVインポート/エクスポート）
    path('shift_requests/import/', views.import_shift_requests_csv, name='import_shift_requests_csv'),
    path('shift_requests/export/', views.export_shift_requests_csv, name='export_shift_requests_csv'),
    path('holiday_requests/import/', views.import_holiday_requests_csv, name='import_holiday_requests_csv'),
    path('holiday_requests/export/', views.export_holiday_requests_csv, name='export_holiday_requests_csv'),
]
