from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserSession

from django.contrib.sessions.models import Session

@receiver(user_logged_in)
def manage_user_session(sender, request, user, **kwargs):
    # Proactively logout other sessions for this user (Auto-Logout)
    try:
        previous_session = UserSession.objects.get(user=user)
        Session.objects.filter(session_key=previous_session.session_key).delete()
    except UserSession.DoesNotExist:
        pass

    # Store the new session key
    UserSession.objects.update_or_create(
        user=user,
        defaults={'session_key': request.session.session_key}
    )

@receiver(user_logged_out)
def clear_user_session(sender, request, user, **kwargs):
    if user:
        UserSession.objects.filter(user=user).delete()
