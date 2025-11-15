from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('dashboard-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('inspect/<int:schedule_id>/', views.inspect_vehicle_form, name='inspect_vehicle'),
    path('print/<int:record_id>/', views.print_inspection, name='print_inspection'),
    path('router/', views.login_router_view, name='login_router'),
]
