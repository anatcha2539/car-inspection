from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InspectionRecord, ProblemReport, Schedule, Vehicle
from .forms import InspectionRecordForm, ProblemReportForm, FUEL_LEVEL_CHOICES
from django.contrib import messages
from django.utils import timezone
from .forms import CHECKLIST_CATEGORIES
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from datetime import timedelta
import json

@login_required
def driver_dashboard(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    weekly_schedules = Schedule.objects.filter(
        driver=request.user, 
        date__range=[start_of_week, end_of_week]
    ).order_by('date', 'vehicle__license_plate')
    
    my_inspections = InspectionRecord.objects.filter(driver=request.user).order_by('-timestamp')[:10]

    context = {
        'todays_schedules': weekly_schedules,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'my_inspections': my_inspections,
    }
    return render(request, 'inspection/dashboard.html', context)
@login_required
def inspect_vehicle_form(request, schedule_id):
    schedule_item = get_object_or_404(
        Schedule, 
        pk=schedule_id, 
        driver=request.user
    )

    if schedule_item.status == 'DONE' and request.method == 'GET':
        messages.info(request, f'รถ {schedule_item.vehicle.license_plate} ตรวจเช็คไปแล้ว')
        return redirect('driver_dashboard')

    vehicle_from_schedule = schedule_item.vehicle
    initial_data = {'vehicle': vehicle_from_schedule}

    if request.method == 'POST':
        inspection_form = InspectionRecordForm(request.POST, initial_vehicle=vehicle_from_schedule)
        problem_form = ProblemReportForm(request.POST) 

        if 'submit_inspection' in request.POST:
            if inspection_form.is_valid():
                record = inspection_form.save(commit=False)
                record.driver = request.user
                record.vehicle = vehicle_from_schedule 
                record.save()

                schedule_item.status = 'DONE'
                schedule_item.save()
                try:
                    vehicle = record.vehicle
                    current_mileage = record.odometer_reading
                    last_service = vehicle.last_service_mileage
                    interval = vehicle.service_interval_km

                    if (current_mileage - last_service >= interval) and (current_mileage > last_service):
                        automated_message = (
                            f"รถถึงระยะเข้าศูนย์ (เลขไมล์ปัจจุบัน: {current_mileage} กม. "
                            f"วิ่งมา {current_mileage - last_service} กม. จากครั้งล่าสุดที่ {last_service} กม.)"
                        )
                        existing_report_exists = ProblemReport.objects.filter(
                            vehicle=vehicle,
                            status='NEW',
                            description__startswith="รถถึงระยะเข้าศูนย์"
                        ).exists()
                        if not existing_report_exists:
                            ProblemReport.objects.create(
                                vehicle=vehicle,
                                reported_by=request.user,
                                description=automated_message,
                                status='NEW'
                            )
                            messages.warning(request, '🔔 ระบบพบว่ารถถึงระยะเข้าศูนย์แล้ว และได้แจ้งเตือนแอดมินอัตโนมัติ')
                            
                except Exception as e:
                    messages.error(request, f'เกิดข้อผิดพลาดในการวิเคราะห์เลขไมล์: {e}')

                messages.success(request, f'✅ บันทึกการตรวจเช็ค {vehicle_from_schedule.license_plate} เรียบร้อย!')
                return redirect('driver_dashboard')
            else:
                messages.error(request, 'ข้อมูลการตรวจเช็คไม่ถูกต้อง กรุณาตรวจสอบ')

        elif 'submit_problem' in request.POST:
            if problem_form.is_valid():
                report = problem_form.save(commit=False)
                report.reported_by = request.user
                report.vehicle = vehicle_from_schedule
                report.save()
                messages.success(request, '🚨 แจ้งปัญหาเรียบร้อย! แอดมินจะตรวจสอบครับ')
                return redirect('inspect_vehicle', schedule_id=schedule_item.pk)
            else:
                messages.error(request, 'ข้อมูลการแจ้งปัญหาไม่ถูกต้อง กรุณาตรวจสอบ')

    else:
        inspection_form = InspectionRecordForm(initial=initial_data, initial_vehicle=vehicle_from_schedule)
        problem_form = ProblemReportForm(initial=initial_data)

    context = {
        'schedule_item': schedule_item,
        'inspection_form': inspection_form,
        'problem_form': problem_form,
    }
    return render(request, 'inspection/inspection_form.html', context)
@login_required
def print_inspection(request, record_id):
    record = get_object_or_404(InspectionRecord, pk=record_id)

    formatted_checklist = {}
    
    for category, items in CHECKLIST_CATEGORIES.items():
        formatted_checklist[category] = []
        for key, label in items:
            status = record.checklist_data.get(key)
            formatted_checklist[category].append({
                'label': label,
                'status': status
            })
    fuel_map = dict(FUEL_LEVEL_CHOICES)
    fuel_key = record.checklist_data.get('fuel_level')
    formatted_fuel_level = fuel_map.get(fuel_key, '-')

    context = {
        'record': record,
        'formatted_checklist': formatted_checklist,
        'today': timezone.now().date(),
        'formatted_fuel_level': formatted_fuel_level,
    }
    return render(request, 'inspection/print_layout.html', context)

@staff_member_required
def admin_dashboard(request):
    today = timezone.now().date()
    total_vehicles = Vehicle.objects.count()
    inspections_today = InspectionRecord.objects.filter(timestamp__date=today).count()
    active_issues = ProblemReport.objects.filter(
        Q(status='NEW') | Q(status='IN_PROGRESS')
    ).count()
    
    problem_stats = ProblemReport.objects.values('status').annotate(count=Count('status'))
    pie_labels = []
    pie_data = []
    for item in problem_stats:
        pie_labels.append(item['status'])
        pie_data.append(item['count'])
    
    last_7_days_data = []
    last_7_days_labels = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = InspectionRecord.objects.filter(timestamp__date=date).count()
        last_7_days_labels.append(date.strftime('%d/%m'))
        last_7_days_data.append(count)

    recent_inspections = InspectionRecord.objects.select_related('vehicle', 'driver').order_by('-timestamp')[:5]
    recent_problems = ProblemReport.objects.filter(status='NEW').order_by('-created_at')[:5]

    context = {
        'total_vehicles': total_vehicles,
        'inspections_today': inspections_today,
        'active_issues': active_issues,
        'pie_labels': json.dumps(pie_labels),
        'pie_data': json.dumps(pie_data),
        'bar_labels': json.dumps(last_7_days_labels),
        'bar_data': json.dumps(last_7_days_data),
        'recent_inspections': recent_inspections,
        'recent_problems': recent_problems,
    }
    return render(request, 'inspection/admin_dashboard.html', context)

@login_required
def login_router_view(request):
    """
    เช็คว่าเป็นแอดมิน หรือ คนขับรถ แล้วส่งไปคนละหน้า
    (ถูกเรียกใช้โดย admin.site.index)
    """
    is_driver = request.user.groups.filter(name='Driver').exists()
    
    if request.user.is_superuser or not is_driver:
        return redirect('admin_dashboard')
    else:
        return redirect('driver_dashboard')