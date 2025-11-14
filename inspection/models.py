from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="ทะเบียนรถ")
    model = models.CharField(max_length=100, verbose_name="รุ่น/ยี่ห้อ")
    vehicle_type = models.CharField(max_length=50, verbose_name="ประเภทรถ", blank=True)
    
    # สำหรับการแจ้งเตือน
    last_service_mileage = models.PositiveIntegerField(default=0, verbose_name="เลขไมล์เข้าศูนย์ครั้งล่าสุด")
    service_interval_km = models.PositiveIntegerField(default=10000, verbose_name="ระยะเข้าศูนย์ (กม.)")

    def __str__(self):
        return f"{self.license_plate} ({self.model})"
    
    class Meta:
        verbose_name = "รถยนต์"
        verbose_name_plural = "ข้อมูลรถยนต์"

class Schedule(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'รอตรวจ'),
        ('DONE', 'ตรวจแล้ว'),
    )
    driver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="คนขับ")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="รถ")
    date = models.DateField(verbose_name="วันที่")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="สถานะ")

    def __str__(self):
        return f"{self.driver.username} - {self.vehicle.license_plate} on {self.date}"
    
    class Meta:
        verbose_name = "ตารางเวร"
        verbose_name_plural = "ตารางเวร"
        unique_together = ('driver', 'vehicle', 'date') # กันตารางซ้ำ

class InspectionRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="รถ")
    driver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="คนขับ")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="วันที่ตรวจ")
    odometer_reading = models.PositiveIntegerField(verbose_name="เลขไมล์ (กม.)")
    remarks = models.TextField(blank=True, null=True, verbose_name="หมายเหตุ")
    checklist_data = models.JSONField(default=dict, verbose_name="ข้อมูล Checklist")

    def __str__(self):
        return f"Record {self.id} - {self.vehicle.license_plate}"
    
    class Meta:
        verbose_name = "บันทึกการตรวจ"
        verbose_name_plural = "ประวัติการตรวจทั้งหมด"

class ProblemReport(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'ใหม่'),
        ('IN_PROGRESS', 'กำลังซ่อม'),
        ('RESOLVED', 'ซ่อมแล้ว'),
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="รถ")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ผู้รายงาน")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่แจ้ง")
    description = models.TextField(verbose_name="รายละเอียดปัญหา")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="สถานะ")
    is_read = models.BooleanField(default=False, verbose_name="แอดมินอ่านแล้ว")

    def __str__(self):
        return f"Problem {self.id} on {self.vehicle.license_plate}"
    
    class Meta:
        verbose_name = "รายงานปัญหา"
        verbose_name_plural = "รายการแจ้งซ่อม"