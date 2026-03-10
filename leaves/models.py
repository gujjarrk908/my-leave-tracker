from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta

class Leave(models.Model):
    STATUS_CHOICES = [
        ('TAKEN', 'Taken'),
        ('PLANNED', 'Planned/Advance'),
    ]
    start_date = models.DateField()
    end_date = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='TAKEN')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def days_count(self):
        # Including both start and end days
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"Leave from {self.start_date} to {self.end_date}"

    @classmethod
    def update_planned_leaves(cls):
        """Marks planned leaves that have passed as taken."""
        cls.objects.filter(
            status='PLANNED',
            end_date__lt=date.today()
        ).update(status='TAKEN')

def get_total_accrued():
    start_accrual = date(2025, 10, 1)
    today = date.today()
    if today < start_accrual:
        return 0
    
    # Calculate difference in months
    diff = relativedelta(today, start_accrual)
    total_months = diff.years * 12 + diff.months + 1 # +1 to include the starting month if we count starting from 1st Oct
    return total_months

def get_leave_summary():
    Leave.update_planned_leaves()
    leaves = Leave.objects.all()
    used_days = sum(leave.days_count for leave in leaves if leave.status == 'TAKEN')
    planned_days = sum(leave.days_count for leave in leaves if leave.status == 'PLANNED')
    accrued = get_total_accrued()
    balance = accrued - used_days - planned_days
    return {
        'accrued': accrued,
        'used': used_days,
        'planned': planned_days,
        'balance': balance,
        'history': leaves.order_by('-start_date')
    }
