from django.shortcuts import render, redirect, get_object_or_404
from .models import Leave, get_leave_summary
from django.contrib import messages
from datetime import datetime

def dashboard(request):
    summary = get_leave_summary()
    return render(request, 'leaves/dashboard.html', {'summary': summary})

def add_leave(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        remarks = request.POST.get('remarks')
        status = request.POST.get('status', 'TAKEN')

        if not start_date_str or not end_date_str:
            messages.error(request, "Please provide both start and end dates.")
            return redirect('add_leave')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if start_date > end_date:
            messages.error(request, "End date cannot be before start date.")
            return render(request, 'leaves/add_leave.html', {
                'start_date': start_date_str,
                'end_date': end_date_str,
                'remarks': remarks,
                'status': status
            })

        try:
            Leave.objects.create(
                start_date=start_date,
                end_date=end_date,
                remarks=remarks,
                status=status
            )
            messages.success(request, "Leave recorded successfully!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('add_leave')

    return render(request, 'leaves/add_leave.html')

def edit_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        remarks = request.POST.get('remarks')
        status = request.POST.get('status')

        if not start_date_str or not end_date_str:
            messages.error(request, "Please provide both start and end dates.")
            return redirect('edit_leave', pk=pk)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if start_date > end_date:
            messages.error(request, "End date cannot be before start date.")
            return render(request, 'leaves/edit_leave.html', {'leave': leave})

        try:
            leave.start_date = start_date
            leave.end_date = end_date
            leave.remarks = remarks
            leave.status = status
            leave.save()
            messages.success(request, "Leave updated successfully!")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('edit_leave', pk=pk)

    return render(request, 'leaves/edit_leave.html', {'leave': leave})
