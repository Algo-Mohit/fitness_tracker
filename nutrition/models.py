"""
NutritionLog model - daily food intake with protein, fat, carbs, calories, water.
"""

from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


class NutritionLog(models.Model):
    """Single food/meal entry: name, macros, calories, water. Per user per date."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutrition_logs')
    date = models.DateField()
    meal_name = models.CharField(max_length=200, help_text='Food or meal description')

    # Macros in grams; calories in kcal
    protein_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fat_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbs_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_calories = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text='Optional: auto from 4*protein + 9*fat + 4*carbs if blank'
    )

    # Water intake for this entry (ml)
    water_ml = models.PositiveIntegerField(default=0, help_text='Water in ml (e.g. 250 for a glass)')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nutrition Log'
        verbose_name_plural = 'Nutrition Logs'
        ordering = ['-date', '-created_at']

    def save(self, *args, **kwargs):
        # Auto-calculate calories from macros if not set: 4 cal/g protein, 4 cal/g carb, 9 cal/g fat
        if self.total_calories is None or self.total_calories == 0:
            p = float(self.protein_g or 0)
            f = float(self.fat_g or 0)
            c = float(self.carbs_g or 0)
            self.total_calories = Decimal(str(round(p * 4 + f * 9 + c * 4, 2)))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.meal_name} - {self.user.username} ({self.date})"
