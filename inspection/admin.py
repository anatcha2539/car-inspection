from django.contrib import admin
from .models import Vehicle, Schedule, InspectionRecord, ProblemReport
from django.utils.html import format_html
from django.urls import reverse

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
    list_display = ('timestamp', 'vehicle', 'driver', 'odometer_reading', 'print_button')
    search_fields = ('vehicle__license_plate', 'vehicle__model', 'driver__username', 'driver__first_name')
    list_filter = ('timestamp', 'driver', 'vehicle')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    readonly_fields = ('checklist_data',)

    def print_button(self, obj):
        url = reverse('print_inspection', args=[obj.id])
        return format_html(
            '<a class="btn btn-sm btn-info" href="{}" target="_blank">'
            '<i class="fas fa-print"></i> พิมพ์ใบตรวจ</a>',
            url
        )

@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'vehicle', 'reported_by', 'status', 'is_read')
    list_filter = ('status', 'created_at', 'is_read')
    search_fields = ('description', 'vehicle__license_plate')
    readonly_fields = ('created_at',)

    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "ทำเครื่องหมายว่าอ่านแล้ว"