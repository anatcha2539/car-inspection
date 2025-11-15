from django import forms
from .models import InspectionRecord, ProblemReport

FUEL_LEVEL_CHOICES = [
    ('5/5', 'เต็มถัง'),
    ('4/5', '3/4'),
    ('3/5', 'ครึ่งถัง'),
    ('2/5', '1/4'),
    ('1/5', 'ใกล้หมด'),
]

CHECKLIST_CATEGORIES = {
    '1. ระบบเครื่องยนต์': [
        ('engine_water', 'น้ำระบายความร้อน'),
        ('engine_oil', 'ระดับน้ำมันเครื่องยนต์'),
        ('engine_air_filter', 'กรองอากาศ'),
        ('engine_belt', 'สายพานเครื่อง'),
        ('engine_brake_fluid', 'น้ำมันเบรค'),
        ('engine_gear_system', 'ระบบเกียร์'),
    ],
    '2. ระบบไฟรถยนต์': [
        ('light_parking', 'ไฟหรี่'),
        ('light_low_beam', 'ไฟต่ำ'),
        ('light_high_beam', 'ไฟสูง'),
        ('light_brake', 'ไฟเบรค'),
        ('light_fog', 'ไฟตัดหมอก'),
        ('light_turn_signal', 'ไฟเลี้ยวขวา/ไฟเลี้ยวซ้าย'),
        ('light_reverse', 'ไฟถอยหลัง'),
        ('light_emergency_horn', 'ไฟสัญญาณฉุกเฉิน/แตร'),
        ('light_cabin', 'ไฟแสงสว่างเก๋ง'),
    ],
    '3. ระบบขับเคลื่อน': [
        ('drive_clutch', 'ระบบคลัทซ์'),
        ('drive_brake_system', 'ระบบเบรค'),
        ('drive_final_gear', 'ระบบเกียร์เฟืองท้าย'),
    ],
    '4. ระบบช่วงล่างและตัวถัง': [
        ('chassis_axle', 'คัชชีและเพลาต่างๆ'),
        ('chassis_paint_body', 'สภาพสีและตัวถัง'),
        ('chassis_tire_pressure', 'แรงดันลมล้อ'),
        ('chassis_side_mirrors', 'กระจกส่องข้างซ้าย/ขวา'),
        ('chassis_rear_mirror', 'กระจกส่องหลัง'),
        ('chassis_seatbelt', 'เข็มขัดนิรภัย'),
    ],
    '5. เครื่องมือและอุปกรณ์': [
        ('tool_spare_tire', 'ยางอะไหล่'),
        ('tool_jack_set', 'เครื่องมือประจำรถ'),
        ('tool_radio', 'วิทยุติดรถยนต์'),
        ('tool_registration', 'สำเนาทะเบียนรถ'),
        ('tool_insurance', 'ประกันภัย, พรบ.'),
        ('tool_fuel_card', 'บัตรเติมน้ำมัน'),
        ('tool_fire_extinguisher', 'ถังดับเพลิง'),
    ],
    '6. อื่นๆ': [
        ('other_fuel', 'น้ำมันเชื้อเพลิง (เต็ม 100%)'),
        ('other_battery', 'ระดับน้ำกลั่น Battery'),
        ('other_wipers', 'ที่ปัดน้ำฝน'),
        ('other_washer_fluid', 'น้ำฉีดล้างกระจก'),
        ('other_ac', 'แอร์รถยนต์'),
    ],
}


class InspectionRecordForm(forms.ModelForm):
    fuel_level = forms.ChoiceField(
        choices=FUEL_LEVEL_CHOICES,
        label='ระดับน้ำมัน',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        
    )
    class Meta:
        model = InspectionRecord
        fields = ['odometer_reading', 'remarks']
        widgets = {
            'odometer_reading': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'เช่น 150000'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 
                                           'placeholder': 'หมายเหตุ หรือ รายการอื่นๆ ที่ไม่ได้อยู่ใน Checklist...'}),
        }

    def __init__(self, *args, **kwargs):
        self.initial_vehicle = kwargs.pop('initial_vehicle', None)
        super().__init__(*args, **kwargs)
        
        self.checklist_fields = {}
        radio_choices = [('OK', 'ปกติ'), ('ISSUE', 'มีปัญหา')]
        
        for category, items in CHECKLIST_CATEGORIES.items():
            self.checklist_fields[category] = []
            for key, label in items:
                field_name = f'checklist_{key}'
                self.fields[field_name] = forms.ChoiceField(
                    choices=radio_choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    label=label,
                    initial='OK',
                    required=True
                )
                self.checklist_fields[category].append(field_name)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        checklist_data = {}
        for key, _ in self.fields.items():
            if key.startswith('checklist_'):
                db_key = key.replace('checklist_', '')
                checklist_data[db_key] = self.cleaned_data.get(key)
        
        if 'fuel_level' in self.cleaned_data:
            checklist_data['fuel_level'] = self.cleaned_data['fuel_level']

        instance.checklist_data = checklist_data
        
        if commit:
            instance.save()
        return instance

class ProblemReportForm(forms.ModelForm):
    class Meta:
        model = ProblemReport
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'อธิบายปัญหาที่พบ...'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.initial_vehicle = kwargs.pop('initial_vehicle', None)
        super().__init__(*args, **kwargs)

