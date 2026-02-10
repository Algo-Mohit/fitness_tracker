"""
URL configuration for fitness_tracker project.
Maps top-level routes to app URL namespaces.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/health/dashboard/', permanent=False)),
    path('', include('users.urls')),
    path('health/', include('health.urls')),
    path('workouts/', include('workouts.urls')),
    path('nutrition/', include('nutrition.urls')),
]
