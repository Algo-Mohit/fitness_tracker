"""
User authentication views: Register, Login, Logout, Profile.
Uses Django auth and login_required where needed.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegisterForm, UserProfileForm
from .models import UserProfile


def register_view(request):
    """Handle user registration and create UserProfile."""
    if request.user.is_authenticated:
        return redirect('health:dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create empty profile linked to new user
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Account created. Complete your profile for better advice.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view - uses our template and redirects to dashboard."""
    template_name = 'users/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    """Log out the user and redirect to login page."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')


@login_required
def profile_view(request):
    """View and edit user profile (age, gender, height, weight, goal)."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('health:dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'form': form, 'profile': profile})
