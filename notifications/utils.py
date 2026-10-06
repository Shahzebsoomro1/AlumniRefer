from .models import Notification


def send_notification(recipient, message, link=''):
    """Helper to create a notification for a user."""
    Notification.objects.create(
        recipient=recipient,
        message=message,
        link=link,
    )
