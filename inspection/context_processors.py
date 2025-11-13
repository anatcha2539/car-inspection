from .models import ProblemReport

def notification_processor(request):
    """
    ตัวประมวลผลที่ส่งข้อมูลการแจ้งเตือนไปยังทุก Template
    """
    pending_problem_count = 0

    if request.user.is_authenticated and request.user.is_staff:

        pending_problem_count = ProblemReport.objects.filter(status='NEW').count()
    return {
        'pending_problem_count': pending_problem_count
    }