from .models import Notification
from django.utils import timezone


def notifications_context_processor(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, read=False).count()
        notifications = Notification.objects.filter(user=request.user).order_by('-datetime')
        latest_notifications = notifications[:5]

        current_time = timezone.now()
        for i in notifications:
            time_difference = current_time - i.datetime
            total_seconds = int(time_difference.total_seconds())

            if total_seconds < 60:
                i.time_ago = f"{total_seconds} seconds ago"
            elif total_seconds < 3600:
                i.time_ago = f"{total_seconds // 60} minutes ago"
            elif total_seconds < 86400:  # Less than 24 hours
                i.time_ago = f"{total_seconds // 3600} hours ago"
            elif total_seconds < 172800:  # Less than 48 hours (1 day)
                i.time_ago = "1 day ago"
            elif total_seconds < 604800:  # Less than a week
                i.time_ago = f"{total_seconds // 86400} days ago"
            elif total_seconds < 1209600:  # Less than 2 weeks (1 week)
                i.time_ago = "1 week ago"
            else:
                weeks = total_seconds // 604800
                i.time_ago = f"{weeks} weeks ago"

            # read true

        for i in notifications:
            i.read = True
            i.save()

        return {
            'unread_count': unread_count,
            'notifications': latest_notifications,
            'all_notifications': notifications,
        }
    return {}