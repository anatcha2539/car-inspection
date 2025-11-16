from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    อนุญาตให้เราเพิ่ม class CSS ให้กับฟิลด์ในฟอร์มของ Django
    """
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='get_field')
def get_field(form, field_name):
    """
    อนุญาตให้เข้าถึงฟิลด์ฟอร์มด้วย "ชื่อ" (string) ในเทมเพลต
    """
    try:
        return form[field_name]
    except KeyError:
        return None