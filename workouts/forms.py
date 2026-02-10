from django import forms
from .models import WorkoutLog


class WorkoutLogForm(forms.ModelForm):
    """Form to add or edit a workout log."""

    class Meta:
        model = WorkoutLog
        fields = ['date', 'exercise_name', 'sets', 'reps', 'duration_minutes', 'location', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exercise_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bench Press'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'reps': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Optional'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional notes'}),
        }
