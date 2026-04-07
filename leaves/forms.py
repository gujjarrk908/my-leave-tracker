from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import UserSession
from django.core.exceptions import ValidationError

class StrictAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()
        
        if user:
            # Check if an active session already exists for this user
            try:
                user_session = UserSession.objects.get(user=user)
                # Verify if the session key is still valid and not expired
                if Session.objects.filter(session_key=user_session.session_key, expire_date__gte=timezone.now()).exists():
                    raise ValidationError(
                        "You are already logged in on another device. Please logout from that device first.",
                        code='already_logged_in'
                    )
                else:
                    # Session exists in mapping but is expired/deleted in Session table
                    user_session.delete()
            except UserSession.DoesNotExist:
                pass
        
        return cleaned_data
