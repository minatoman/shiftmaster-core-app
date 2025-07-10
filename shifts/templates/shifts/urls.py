# shifts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 🌐 ホーム & 認証（トップに置く）
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile, name='profile'),

    # 📋 シフト管理
    path('list/', views.shift_list, name='shift_list'),
    path('add/', views.add_shift, name='add_shift'),
    path('edit/<int:shift_id>/', views.edit_shift, name='edit_shift'),
    path('delete/<int:shift_id>/', views.delete_shift, name='delete_shift'),
    path('confirm_delete/<int:shift_id>/', views.confirm_delete_shift, name='confirm_delete_shift'),
    path('approve/<int:shift_id>/', views.approve_shift, name='approve_shift'),

    # 🤖 自動割当 & 出力
    path('auto_assign/', views.auto_assign, name='auto_assign'),
    path('export/pdf/', views.export_shift_pdf, name='export_shift_pdf'),

    # 📥 シフトCSVアップロード & エラー
    path('upload_csv/', views.upload_shifts_csv, name='upload_shifts_csv'),
    path('error_log/download/', views.download_error_log_csv, name='download_error_log_csv'),

    # 📄 テンプレート表示
    path('template/3block/', views.view_generated_shift_template, name='shift_template_3block'),

    # 📊 月次集計 & ダッシュボード
    path('summary/monthly/', views.monthly_shift_summary, name='monthly_shift_summary'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 📩 勤務希望
    path('requests/', views.shift_request_list, name='shift_request_list'),
    path('holidays/add/', views.add_holiday_request, name='add_holiday_request'),
    path('requests/export/csv/', views.export_shift_requests_csv, name='export_shift_requests_csv'),
    path('requests/export/excel/', views.export_shift_requests_excel, name='export_shift_requests_excel'),
    path('requests/import/csv/', views.import_shift_requests_csv, name='import_shift_requests_csv'),
    path('requests/import/excel/', views.import_shift_requests_excel, name='import_shift_requests_excel'),
    path('api/shift_request/', views.shift_request_api, name='shift_request_api'),

    # 📅 カレンダー
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/events/', views.calendar_event_api, name='calendar_event_api'),

    # 🧭 テンプレートリンク確認
    path('templates/', views.template_links_view, name='template_links'),
]


