"""
Health dashboard and calculations view.
Shows BMI, BMR, calories, macros, workout/nutrition summary, and smart advice.
"""

from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from users.models import UserProfile
from workouts.models import WorkoutLog
from nutrition.models import NutritionLog

from .models import HealthData
from .calculations import compute_all_health_metrics
from .advice import collect_all_advice


@login_required
def dashboard_view(request):
    """
    Main dashboard: show health metrics, recent workouts, nutrition summary,
    and personalized advice. Requires profile (height, weight, age, gender) for calculations.
    """
    profile = None
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        pass

    # If profile incomplete, redirect to profile page
    if not profile or profile.height is None or profile.weight is None or profile.age is None or not profile.gender:
        messages.info(request, 'Complete your profile (age, gender, height, weight) to see your dashboard.')
        return redirect('users:profile')

    # Get latest health metrics (compute from profile)
    weight_kg = float(profile.weight)
    height_cm = float(profile.height)
    age = profile.age
    gender = profile.gender
    goal = profile.goal or 'maintain'

    metrics = compute_all_health_metrics(weight_kg, height_cm, age, gender, goal)

    # Save snapshot to HealthData once per day (for history)
    today = timezone.now().date()
    if not HealthData.objects.filter(user=request.user, created_at__date=today).exists():
        HealthData.objects.create(
            user=request.user,
            weight=profile.weight,
            height=profile.height,
            age=age,
            gender=gender,
            goal=goal,
            bmi=metrics['bmi'],
            bmi_category=metrics['bmi_category'],
            bmr=metrics['bmr'],
            daily_calories=metrics['daily_calories'],
            daily_protein_g=metrics['daily_protein_g'],
            daily_fat_g=metrics['daily_fat_g'],
            daily_carbs_g=metrics['daily_carbs_g'],
            daily_water_liters=metrics['daily_water_liters'],
        )

    # Today's nutrition totals (convert to float to avoid Decimal/float mix in advice)
    today = timezone.now().date()
    nutrition_today = NutritionLog.objects.filter(user=request.user, date=today)
    consumed_calories = float(sum(n.total_calories or 0 for n in nutrition_today))
    consumed_protein = float(sum(n.protein_g or 0 for n in nutrition_today))
    consumed_fat = float(sum(n.fat_g or 0 for n in nutrition_today))
    consumed_carbs = float(sum(n.carbs_g or 0 for n in nutrition_today))
    consumed_water = float(sum(n.water_ml or 0 for n in nutrition_today)) / 1000.0  # liters

    required_protein = float(metrics['daily_protein_g'])
    required_water = float(metrics['daily_water_liters'])

    # Smart advice
    advice_list = collect_all_advice(
        metrics['bmi'],
        metrics['bmi_category'],
        goal,
        consumed_protein=consumed_protein,
        required_protein=required_protein,
        consumed_water=consumed_water,
        required_water=required_water,
    )

    # Recent workouts (last 7 days)
    from django.db.models import Sum
    from datetime import timedelta
    week_ago = today - timedelta(days=7)
    recent_workouts = WorkoutLog.objects.filter(user=request.user, date__gte=week_ago).order_by('-date', '-id')[:10]
    workout_summary = WorkoutLog.objects.filter(user=request.user, date__gte=week_ago).aggregate(
        total_sets=Sum('sets'),
        total_reps=Sum('reps'),
    )
    # Ensure no None in template (aggregate returns None when no rows)
    if workout_summary['total_sets'] is None:
        workout_summary['total_sets'] = 0
    if workout_summary['total_reps'] is None:
        workout_summary['total_reps'] = 0

    # Progress percentages for bars (cap at 100 for display)
    def pct(consumed, required):
        c, r = float(consumed), float(required)
        if not r or r <= 0:
            return 0
        return min(100, round(100 * c / r))

    context = {
        'profile': profile,
        'metrics': metrics,
        'advice_list': advice_list,
        'consumed_calories': consumed_calories,
        'consumed_protein': consumed_protein,
        'consumed_fat': consumed_fat,
        'consumed_carbs': consumed_carbs,
        'consumed_water': consumed_water,
        'required_calories': float(metrics['daily_calories']),
        'required_protein': required_protein,
        'required_fat': float(metrics['daily_fat_g']),
        'required_carbs': float(metrics['daily_carbs_g']),
        'required_water': required_water,
        'progress_calories': pct(consumed_calories, float(metrics['daily_calories'])),
        'progress_protein': pct(consumed_protein, required_protein),
        'progress_water': pct(consumed_water, required_water),
        'recent_workouts': recent_workouts,
        'workout_summary': workout_summary,
        'nutrition_today': nutrition_today,
    }
    return render(request, 'health/dashboard.html', context)
