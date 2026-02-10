"""
HealthData model - stores calculated health metrics per user.
Used for history and displaying latest calculations on dashboard.
"""

from django.db import models
from django.contrib.auth.models import User


class HealthData(models.Model):
    """
    Stores snapshot of health calculations for a user.
    Linked to user profile data at time of calculation.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_data')

    # Inputs used for calculation
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # kg
    height = models.DecimalField(max_digits=5, decimal_places=2)  # cm
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1)  # M or F
    goal = models.CharField(max_length=10)

    # Calculated outputs
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bmi_category = models.CharField(max_length=20, null=True, blank=True)
    bmr = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # kcal/day
    daily_calories = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    daily_protein_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    daily_fat_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    daily_carbs_g = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    daily_water_liters = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Health Data'
        verbose_name_plural = 'Health Data'
        ordering = ['-created_at']

    def __str__(self):
        return f"Health data for {self.user.username} at {self.created_at.date()}"
