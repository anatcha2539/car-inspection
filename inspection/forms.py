from django import forms
from .models import InspectionRecord, ProblemReport, Vehicle

CHECKLIST_CATEGORIES = {
    '1. ระบบเครื่องยนต์': [
        ('engine_coolant', 'น้ำระบายความร้อน'),
        ('engine_oil', 'ระดับน้ำมันเครื่องยนต์'),
        ('engine_air_filter', 'กรองอากาศ'),
        ('engine_belt', 'สายพานเครื่อง'),
        ('engine_brake_fluid', 'น้ำมันเบรค'),
        ('engine_gear', 'ระบบเกียร์'),
    ],
    '2. ระบบไฟรถยนต์': [
        ('lights_parking', 'ไฟหรี่'),
        ('lights_low_beam', 'ไฟต่ำ'),
        ('lights_high_beam', 'ไฟสูง'),
        ('lights_brake', 'ไฟเบรค'),
        ('lights_fog', 'ไฟตัดหมอก'),
        ('lights_turn', 'ไฟเลี้ยวขวา/ซ้าย'),
        ('lights_reverse', 'ไฟถอยหลัง'),
        ('lights_emergency', 'ไฟสัญญาณฉุกเฉิน/แตร'),
        ('lights_cabin', 'ไฟแสงสว่างเก๋ง'),
    ],
    '3. ระบบขับเคลื่อน': [
        ('drive_clutch', 'ระบบคลัทซ์'),
        ('drive_brake', 'ระบบเบรค'),
        ('drive_differential', 'ระบบเกียร์เฟืองท้าย'),
    ],
    '4. ระบบช่วงล่างและตัวถัง': [
        ('body_chassis', 'คัซซีและเพลาต่างๆ'),
        ('body_paint', 'สภาพสีและตัวถัง'),
        ('body_tire_pressure', 'แรงดันลมล้อ'),
        ('body_mirrors', 'กระจกส่องข้างซ้าย/ขวา'),
        ('body_rear_mirror', 'กระจกส่องหลัง'),
        ('body_seatbelt', 'เข็มขัดนิรภัย'),
    ],
    '5. เครื่องมือและอุปกรณ์ประจำรถ': [
        ('tools_spare_tire', 'ยางอะไหล์'),
        ('tools_jack', 'เครื่องมือประจำรถ'),
        ('tools_radio', 'วิทยุติดรถยนต์'),
        ('tools_registration', 'สำเนาทะเบียนรถ'),
        ('tools_insurance', 'ประกันภัย, พรบ.'),
        ('tools_fuel_card', 'บัตรเติมน้ำมัน'),
        ('tools_fire_extinguisher', 'ถังดับเพลิง'),
    ],
}


class InspectionRecordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.initial_vehicle = kwargs.pop('initial_vehicle', None) 
        super().__init__(*args, **kwargs)
        
        self.fields['odometer_reading'].widget.attrs.update({'class': 'form-control'})
        self.fields['fuel_level'].widget.attrs.update({'class': 'form-select'})
        self.fields['notes'].widget.attrs.update({'class': 'form-control'})

        if self.initial_vehicle:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(pk=self.initial_vehicle.pk)
            self.fields['vehicle'].widget.attrs.update({'class': 'form-select', 'disabled': True})
            self.fields['vehicle'].empty_label = None
            self.fields['vehicle'].required = False
        else:
            self.fields['vehicle'].queryset = Vehicle.objects.none()
            self.fields['vehicle'].required = False
        self.checklist_fields = []
        for category, items in CHECKLIST_CATEGORIES.items():
            for field_name, field_label in items:
                self.fields[field_name] = forms.BooleanField(
                    required=False, 
                    label=field_label,
                    initial=True,
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
                )
                self.checklist_fields.append(field_name)

        self.CHECKLIST_CATEGORIES = CHECKLIST_CATEGORIES 

    class Meta:
        model = InspectionRecord
        fields = ['vehicle', 'odometer_reading', 'fuel_level', 'notes'] 
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'หมายเหตุเพิ่มเติม (ถ้ามี)'}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.initial_vehicle:
            instance.vehicle = self.initial_vehicle
            
        checklist_data = {}
        for field_name in self.checklist_fields:
            checklist_data[field_name] = self.cleaned_data.get(field_name)
        instance.checklist_data = checklist_data
        
        if commit:
            instance.save()
        return instance


class ProblemReportForm(forms.ModelForm):
    class Meta:
        model = ProblemReport
        fields = ['vehicle', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'อธิบายปัญหาที่พบ...'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.initial_vehicle = kwargs.pop('initial_vehicle', None)
        super().__init__(*args, **kwargs)
        
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

        if self.initial_vehicle:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(pk=self.initial_vehicle.pk)
            self.fields['vehicle'].widget.attrs.update({'class': 'form-select', 'disabled': True})
            self.fields['vehicle'].empty_label = None
            self.fields['vehicle'].required = False 
        else:
            self.fields['vehicle'].queryset = Vehicle.objects.none()
            self.fields['vehicle'].required = False # <--- 
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.initial_vehicle:
            instance.vehicle = self.initial_vehicle
        if commit:
            instance.save()
        return instance