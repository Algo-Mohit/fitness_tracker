"""
User profile model - stores fitness-related user data.
Extends Django's built-in User with age, gender, height, weight, and goal.
"""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile for fitness tracking (age, gender, height, weight, goal)."""

    # One-to-one link with Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Demographics and body metrics
    age = models.PositiveIntegerField(null=True, blank=True, help_text='Age in years')
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    height = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text='Height in cm'
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text='Weight in kg'
    )

    # Fitness goal
    GOAL_CHOICES = [
        ('lose', 'Lose Weight'),
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Weight'),
    ]
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, default='maintain')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"Profile of {self.user.username}"
