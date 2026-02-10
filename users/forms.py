"""
User registration and profile forms with validation.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    """Registration form - username, email, password with validation."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    """Form to edit user profile (age, gender, height, weight, goal)."""

    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'height', 'weight', 'goal']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 120}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'min': 50, 'max': 300, 'step': 0.1}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': 20, 'max': 500, 'step': 0.1}),
            'goal': forms.Select(attrs={'class': 'form-select'}),
        }
