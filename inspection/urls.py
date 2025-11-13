from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.driver_dashboard, name='driver_dashboard'),

    path('inspect/<int:schedule_id>/', views.inspect_vehicle_form, name='inspect_vehicle'),

    path('print/<int:record_id>/', views.print_inspection, name='print_inspection'),

    path('dashboard-admin/', views.admin_dashboard, name='admin_dashboard'),
]