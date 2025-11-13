from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="ทะเบียนรถ")
    model = models.CharField(max_length=100, verbose_name="รุ่นรถ")

    last_service_mileage = models.IntegerField(default=0, verbose_name="เลขไมล์ที่เข้าศูนย์ล่าสุด")
    service_interval_km = models.IntegerField(default=10000, verbose_name="ระยะที่ต้องเข้าศูนย์ (กม.)")

    def __str__(self):
        return f"{self.license_plate} ({self.model})"
    
class InspectionRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="รถที่ตรวจ")
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="พนักงานขับรถ")

    odometer_reading = models.IntegerField(verbose_name="เลขไม่ปัจจุบัน")
    FUEL_LEVEL_CHOICES = [
        ('F', 'เต็มถัง (F)'),
        ('3/4', '3/4'),
        ('1/2', 'ครึ่งถัง (1/2)'),
        ('1/4', '1/4'),
        ('E', 'ใกล้หมด (E)'),
    ]
    fuel_level = models.CharField(
        max_length=5,
        choices=FUEL_LEVEL_CHOICES,
        default='F',
        verbose_name="ระดับน้ำมัน"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="หมายเหตุอื่นๆ")

    checklist_data = models.JSONField(null=True, blank=True, verbose_name="ข้อมูลเช็คลิสต์")

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="เวลาที่บันทึก")

    def __str__(self):
        return f"ตรวจ {self.vehicle.license_plate} - {self.timestamp.strftime('%Y-%m-%d')}"

class ProblemReport(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'แจ้งใหม่'),
        ('IN_PROGRESS', 'กำลังดำเนินการ'),
        ('RESOLVED', 'แก้ไขแล้ว')
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="รถที่พบปัญหา")
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="ผู้แจ้ง")
    description = models.TextField(verbose_name="รายละเอียดปัญหา")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="สถานะ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ปัญหา {self.vehicle.license_plate} ({self.status})"
    
class Schedule(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="พนักงานขับรถ")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="รถที่ต้องตรวจ")
    date = models.DateField(default=timezone.now, verbose_name="วันที่ตรวจ")

    STATUS_CHOICES = [('PENDING', 'ยังไม่ตรวจ'), ('DONE', 'ตรวจแล้ว')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        unique_together = ('driver', 'vehicle', 'date')
        verbose_name = "ตารางเวร"
        verbose_name_plural = "ตารางเวร"

    def __str__(self):
        return f"{self.date}: {self.driver.username} -> {self.vehicle.license_plate}"