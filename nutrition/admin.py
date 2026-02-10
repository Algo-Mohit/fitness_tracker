from django.contrib import admin
from .models import NutritionLog


@admin.register(NutritionLog)
class NutritionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'meal_name', 'protein_g', 'fat_g', 'carbs_g', 'total_calories']
    list_filter = ['date']
    search_fields = ['user__username', 'meal_name']
