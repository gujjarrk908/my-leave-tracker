import os
import django
from datetime import date
from django.test import Client, RequestFactory
from django.urls import reverse
from django.contrib.messages import get_messages

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leave_tracker.settings')
django.setup()

from leaves.models import Leave

def test_new_features():
    client = Client()
    
    # 1. Test Date Validation in Add Leave
    print("Testing Date Validation (Add Leave)...")
    response = client.post(reverse('add_leave'), {
        'start_date': '2026-05-10',
        'end_date': '2026-05-05', # Invalid: end < start
        'remarks': 'Invalid Range'
    })
    messages = list(get_messages(response.wsgi_request))
    assert any("End date cannot be before start date." in str(m) for m in messages)
    print("Add Leave validation passed!")

    # 2. Test Edit Functionality
    print("Testing Edit Functionality...")
    # Create a leave first
    l = Leave.objects.create(start_date=date(2026, 6, 1), end_date=date(2026, 6, 1), remarks="Original")
    
    # Edit it
    response = client.post(reverse('edit_leave', kwargs={'pk': l.pk}), {
        'start_date': '2026-06-01',
        'end_date': '2026-06-05', # Extend to 5 days
        'remarks': 'Updated'
    })
    
    l.refresh_from_db()
    assert l.days_count == 5
    assert l.remarks == 'Updated'
    print("Edit functionality passed!")

    # 3. Test Date Validation in Edit Leave
    print("Testing Date Validation (Edit Leave)...")
    response = client.post(reverse('edit_leave', kwargs={'pk': l.pk}), {
        'start_date': '2026-06-10',
        'end_date': '2026-06-05', # Invalid
    })
    messages = list(get_messages(response.wsgi_request))
    assert any("End date cannot be before start date." in str(m) for m in messages)
    print("Edit validation passed!")

    # Cleanup
    l.delete()
    print("All tests passed!")

if __name__ == "__main__":
    test_new_features()
