from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'shifts'

urlpatterns = [
    # 認証関連
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='shifts:home'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/password_change/done/'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),
    
    # メイン機能
    path('dashboard/', views.dashboard, name='dashboard'),
    path('calendar/', views.shift_calendar, name='calendar'),
    path('shifts/', views.shift_list, name='shift_list'),
    path('shifts/create/', views.shift_create, name='shift_create'),
    path('shifts/quick-create/', views.quick_shift_create, name='quick_shift_create'),
    
    # 申請関連
    path('requests/', views.request_list, name='request_list'),
    path('requests/create/', views.shift_request_create, name='request_create'),
    
    # 出勤打刻
    path('attendance/punch/', views.attendance_punch, name='attendance_punch'),
    
    # プロフィール
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # 通知
    path('notifications/', views.notifications, name='notifications'),
    
    # API
    path('api/shifts/', views.api_shift_data, name='api_shift_data'),
]
