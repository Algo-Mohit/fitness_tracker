from django.contrib import admin
from .models import WorkoutLog


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'exercise_name', 'sets', 'reps', 'location']
    list_filter = ['date', 'location']
    search_fields = ['user__username', 'exercise_name']
