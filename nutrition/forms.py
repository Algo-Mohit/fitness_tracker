from django import forms
from .models import NutritionLog


class NutritionLogForm(forms.ModelForm):
    """Form to add or edit a nutrition log."""

    class Meta:
        model = NutritionLog
        fields = ['date', 'meal_name', 'protein_g', 'fat_g', 'carbs_g', 'total_calories', 'water_ml']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'meal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Chicken breast, rice'}),
            'protein_g': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.1}),
            'fat_g': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.1}),
            'carbs_g': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.1}),
            'total_calories': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01, 'placeholder': 'Auto from macros if blank'}),
            'water_ml': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'e.g. 250 for a glass'}),
        }
