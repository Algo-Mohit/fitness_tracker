from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.nutrition_list_view, name='list'),
    path('add/', views.nutrition_add_view, name='add'),
    path('<int:pk>/edit/', views.nutrition_edit_view, name='edit'),
    path('<int:pk>/delete/', views.nutrition_delete_view, name='delete'),
]
