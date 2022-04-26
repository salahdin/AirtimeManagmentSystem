from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.register_employee, name='add_user'),
    path('transactions/',views.view_transaction,name="transactions"),
    path('billing/',views.billing,name="billing"),
    path('topup/', views.single_topup, name="single_topup")
]