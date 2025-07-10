# dialysis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dialysis_daily_view, name='dialysis_daily'),
    path('register/', views.dialysis_register_view, name='dialysis_register'),
    path('import/', views.import_dialysis_csv, name='import_dialysis_csv'),
    path('<str:selected_date>/', views.dialysis_daily_view, name='dialysis_daily_date'),
    path('export/pdf/<str:date_str>/', views.dialysis_pdf_export, name='dialysis_pdf_export'),
    path('calendar/', views.dialysis_calendar_api_events, name='dialysis_calendar_api'),
]

