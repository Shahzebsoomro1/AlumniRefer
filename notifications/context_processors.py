from .models import Notification


def unread_notifications(request):
    """Context processor: inject unread notification count into every template."""
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        recent = Notification.objects.filter(
            recipient=request.user
        )[:5]
        return {
            'unread_notification_count': count,
            'recent_notifications': recent,
        }
    return {
        'unread_notification_count': 0,
        'recent_notifications': [],
    }
