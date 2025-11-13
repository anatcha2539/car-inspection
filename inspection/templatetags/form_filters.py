from django import template

register = template.Library()

@register.filter(name='get_field')
def get_field(form, field_name):
    """
    ดึงฟิลด์จากฟอร์มด้วยชื่อที่เป็น string
    """
    return form[field_name]

@register.filter(name='get_field_id')
def get_field_id(form, field_name):
    """
    ดึง ID ของฟิลด์สำหรับ <label>
    """
    return form[field_name].id_for_label