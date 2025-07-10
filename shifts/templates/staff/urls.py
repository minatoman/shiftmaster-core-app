# staff/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_create, name='employee_create'),
    path('upload/', views.upload_employee_csv, name='upload_employee_csv'),
    path('edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('detail/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('delete_duplicates/', views.delete_duplicates, name='delete_duplicates'),
    path('upload_fixture/', views.upload_fixture, name='upload_fixture'),
]

