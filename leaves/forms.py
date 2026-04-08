from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import UserSession
from django.core.exceptions import ValidationError

class StrictAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        # Blocking logic removed - session clearing handled in signals.py
        return cleaned_data
