from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Vehicle, InspectionRecord, ProblemReport, Schedule
from .forms import CHECKLIST_CATEGORIES

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'model', 'last_service_mileage', 'service_interval_km')
    search_fields = ('license_plate', 'model')

class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'status', 'reported_by', 'created_at')
    list_filter = ('status', 'vehicle')
    search_fields = ('description', 'vehicle__license_plate')
    date_hierarchy = 'created_at'

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'driver', 'vehicle', 'status')
    list_filter = ('date', 'driver', 'vehicle', 'status')
    search_fields = ('driver__username', 'vehicle__license_plate')
    date_hierarchy = 'date'

class InspectionRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'driver', 'timestamp', 'odometer_reading', 'fuel_level', 'print_report_button')
    list_filter = ('vehicle', 'driver', 'timestamp')
    search_fields = ('vehicle__license_plate', 'driver__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('display_checklist', 'print_report_button') 
    exclude = ('checklist_data',)
    fieldsets = (
        ('ข้อมูลหลัก', {
            'fields': ('vehicle', 'driver', 'odometer_reading', 'fuel_level', 'notes')
        }),
        ('การจัดการเอกสาร', {
            'fields': ('print_report_button',)
        }),
        ('ผลการตรวจเช็ค (Read-Only)', {
            'fields': ('display_checklist',) 
        }),
    )
    def print_report_button(self, obj):
        url = reverse('print_inspection', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" target="_blank" style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;">🖨️ พิมพ์ PDF</a>', 
            url
        )
    
    print_report_button.short_description = "พิมพ์รายงาน"
    print_report_button.allow_tags = True
    def display_checklist(self, obj):
        if not obj.checklist_data:
            return "ไม่มีข้อมูลเช็คลิสต์"

        html = '<div style="max-height: 400px; overflow-y: auto; border: 1px solid #eee; padding: 10px;">'
        
        for category, items in CHECKLIST_CATEGORIES.items():
            html += f'<h6 style="margin-top: 10px; font-weight:bold;">{category}</h6>'
            html += '<ul style="list-style-type: none; padding-left: 15px;">'
            
            for field_name, field_label in items:
                status = obj.checklist_data.get(field_name, None)
                
                if status == True:
                    icon = '✅'
                    color = '#28a745'
                elif status == False:
                    icon = '❌'
                    color = '#dc3545'
                else:
                    icon = '❓'
                    color = '#6c757d'
                    
                html += f'<li style="color: {color}; margin-bottom: 5px;">{icon} {field_label}</li>'
            
            html += '</ul>'
        
        html += '</div>'
        return mark_safe(html)
    
    display_checklist.short_description = "รายละเอียดผลการตรวจ"
    
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(ProblemReport, ProblemReportAdmin)
admin.site.register(InspectionRecord, InspectionRecordAdmin)
admin.site.register(Schedule, ScheduleAdmin)