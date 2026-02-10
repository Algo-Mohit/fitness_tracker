"""
WorkoutLog model - stores daily workouts (exercise, sets, reps, duration).
Supports home and gym workout types.
"""

from django.db import models
from django.contrib.auth.models import User


class WorkoutLog(models.Model):
    """Single workout entry: exercise name, sets, reps, duration, location (home/gym)."""

    LOCATION_CHOICES = [
        ('home', 'Home'),
        ('gym', 'Gym'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_logs')
    date = models.DateField()
    exercise_name = models.CharField(max_length=200)
    sets = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField(default=0, help_text='Reps per set (use 0 if duration-based)')
    duration_minutes = models.PositiveIntegerField(
        null=True, blank=True,
        help_text='Duration in minutes (for cardio/time-based exercises)'
    )
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='gym')
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Workout Log'
        verbose_name_plural = 'Workout Logs'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.exercise_name} - {self.user.username} ({self.date})"
