from .models import ProblemReport

def notification_processor(request):
    if request.user.is_authenticated and request.user.is_staff:
        new_problems_count = ProblemReport.objects.filter(
            status='NEW', 
            is_read=False
        ).count()
        recent_problems = ProblemReport.objects.filter(
            status='NEW',
            is_read=False
        ).order_by('-created_at')[:5]
        
        return {
            'new_problems_count': new_problems_count,
            'recent_problems_list': recent_problems,
        }
    return {}