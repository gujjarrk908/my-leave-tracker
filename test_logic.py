import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leave_tracker.settings')
django.setup()

from leaves.models import Leave, get_total_accrued, get_leave_summary

def test_calculations():
    print("Testing Leave Accrual Logic...")
    accrued = get_total_accrued()
    print(f"Total accrued since Oct 1, 2025: {accrued}")
    
    # Test adding a leave
    print("Adding a sample leave...")
    start = date(2026, 1, 10)
    end = date(2026, 1, 12)
    l = Leave.objects.create(start_date=start, end_date=end, remarks="Test")
    
    summary = get_leave_summary()
    print(f"Summary: Accrued={summary['accrued']}, Used={summary['used']}, Balance={summary['balance']}")
    
    assert summary['used'] == 3 # 10, 11, 12
    assert summary['balance'] == accrued - 3
    
    print("Test Passed!")
    
    # Cleanup
    l.delete()

if __name__ == "__main__":
    test_calculations()
