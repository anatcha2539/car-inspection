from django.contrib import admin
from .models import Vehicle, Schedule, InspectionRecord, ProblemReport

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'model', 'vehicle_type', 'last_service_mileage', 'service_interval_km')
    search_fields = ('license_plate', 'model')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'driver', 'vehicle', 'status')
    list_filter = ('date', 'status', 'driver')
    search_fields = ('driver__username', 'vehicle__license_plate')
    date_hierarchy = 'date'

@admin.register(InspectionRecord)
class InspectionRecordAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'vehicle', 'driver', 'odometer_reading')
    list_filter = ('timestamp', 'driver', 'vehicle')
    date_hierarchy = 'timestamp'
    readonly_fields = ('checklist_data',)

@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'vehicle', 'reported_by', 'status', 'is_read')
    list_filter = ('status', 'created_at', 'is_read')
    search_fields = ('description', 'vehicle__license_plate')
    readonly_fields = ('created_at',)