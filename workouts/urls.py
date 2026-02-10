from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.workout_list_view, name='list'),
    path('add/', views.workout_add_view, name='add'),
    path('<int:pk>/edit/', views.workout_edit_view, name='edit'),
    path('<int:pk>/delete/', views.workout_delete_view, name='delete'),
]
