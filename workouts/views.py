"""
Workout views: list history, add workout, delete workout.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import WorkoutLog
from .forms import WorkoutLogForm


@login_required
def workout_list_view(request):
    """List user's workout history with pagination."""
    logs = WorkoutLog.objects.filter(user=request.user).order_by('-date', '-id')
    paginator = Paginator(logs, 15)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    return render(request, 'workouts/workout_list.html', {'page_obj': page_obj})


@login_required
def workout_add_view(request):
    """Add a new workout log."""
    if request.method == 'POST':
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Workout added successfully.')
            return redirect('workouts:list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = WorkoutLogForm()
    return render(request, 'workouts/workout_form.html', {'form': form, 'title': 'Add Workout'})


@login_required
def workout_edit_view(request, pk):
    """Edit an existing workout log."""
    log = get_object_or_404(WorkoutLog, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkoutLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout updated.')
            return redirect('workouts:list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = WorkoutLogForm(instance=log)
    return render(request, 'workouts/workout_form.html', {'form': form, 'title': 'Edit Workout', 'log': log})


@login_required
def workout_delete_view(request, pk):
    """Delete a workout log."""
    log = get_object_or_404(WorkoutLog, pk=pk, user=request.user)
    if request.method == 'POST':
        log.delete()
        messages.success(request, 'Workout deleted.')
        return redirect('workouts:list')
    return render(request, 'workouts/workout_confirm_delete.html', {'log': log})
