from django.contrib import admin
from .models import HealthData


@admin.register(HealthData)
class HealthDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'bmi', 'bmi_category', 'bmr', 'daily_calories', 'created_at']
    list_filter = ['bmi_category', 'goal']
    search_fields = ['user__username']
