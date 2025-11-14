from .models import ProblemReport

def notification_processor(request):
    if request.user.is_authenticated and request.user.is_staff:
        # นับปัญหาใหม่ที่ยังไม่ถูกอ่าน
        new_problems_count = ProblemReport.objects.filter(
            status='NEW', 
            is_read=False
        ).count()
        
        # ดึงปัญหา 5 รายการล่าสุดมาแสดง
        recent_problems = ProblemReport.objects.filter(
            status='NEW',
            is_read=False
        ).order_by('-created_at')[:5]
        
        return {
            'new_problems_count': new_problems_count,
            'recent_problems_list': recent_problems,
        }
    return {}