"""
Nutrition views: list logs, add, edit, delete. Compare required vs consumed macros.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum

from users.models import UserProfile
from health.calculations import compute_all_health_metrics

from .models import NutritionLog
from .forms import NutritionLogForm


def _get_required_macros(request):
    """Get user's required calories and macros from profile; None if profile incomplete."""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return None
    if profile.height is None or profile.weight is None or profile.age is None or not profile.gender:
        return None
    metrics = compute_all_health_metrics(
        float(profile.weight), float(profile.height), profile.age,
        profile.gender, profile.goal or 'maintain'
    )
    return metrics


@login_required
def nutrition_list_view(request):
    """List user's nutrition logs with optional date filter; show required vs consumed for today."""
    logs = NutritionLog.objects.filter(user=request.user).order_by('-date', '-id')[:50]
    required = _get_required_macros(request)
    today = timezone.now().date()
    today_logs = NutritionLog.objects.filter(user=request.user, date=today)
    consumed = {
        'calories': sum(n.total_calories or 0 for n in today_logs),
        'protein': sum(n.protein_g or 0 for n in today_logs),
        'fat': sum(n.fat_g or 0 for n in today_logs),
        'carbs': sum(n.carbs_g or 0 for n in today_logs),
        'water_ml': sum(n.water_ml or 0 for n in today_logs),
    }
    context = {
        'logs': logs,
        'required': required,
        'consumed': consumed,
        'today': today,
    }
    return render(request, 'nutrition/nutrition_list.html', context)


@login_required
def nutrition_add_view(request):
    """Add a new nutrition log."""
    if request.method == 'POST':
        form = NutritionLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Food entry added.')
            return redirect('nutrition:list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = NutritionLogForm(initial={'date': timezone.now().date()})
    return render(request, 'nutrition/nutrition_form.html', {'form': form, 'title': 'Add Food Entry'})


@login_required
def nutrition_edit_view(request, pk):
    """Edit an existing nutrition log."""
    log = get_object_or_404(NutritionLog, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NutritionLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated.')
            return redirect('nutrition:list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = NutritionLogForm(instance=log)
    return render(request, 'nutrition/nutrition_form.html', {'form': form, 'title': 'Edit Entry', 'log': log})


@login_required
def nutrition_delete_view(request, pk):
    """Delete a nutrition log."""
    log = get_object_or_404(NutritionLog, pk=pk, user=request.user)
    if request.method == 'POST':
        log.delete()
        messages.success(request, 'Entry deleted.')
        return redirect('nutrition:list')
    return render(request, 'nutrition/nutrition_confirm_delete.html', {'log': log})
