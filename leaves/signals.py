from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserSession

@receiver(user_logged_in)
def manage_user_session(sender, request, user, **kwargs):
    # After user logs in, store their new session key
    UserSession.objects.update_or_create(
        user=user,
        defaults={'session_key': request.session.session_key}
    )

@receiver(user_logged_out)
def clear_user_session(sender, request, user, **kwargs):
    if user:
        UserSession.objects.filter(user=user).delete()
