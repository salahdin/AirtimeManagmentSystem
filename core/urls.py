from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.register_employee, name='add_user'),
    path('transactions/', views.view_transaction, name="transactions"),
    path('billing/', views.billing, name="billing"),
    path('topup/<int:employee_id>/', views.single_topup, name="single_topup"),
    path('bulktopup/', views.bulk_topup, name="bulk_topup"),
    path('employee/<int:employee_id>/', views.employee_detail, name="employee_detail"),
    path('generate_report/', views.generate_pdf_report, name="generate report"),
    path('delete/<int:id>/', views.delete_employee, name="delete_employee"),
    path('bulk_register/', views.upload_employees,name="upload_employee")
]
