from django.urls import path
from . import views

urlpatterns = [
    path('get_categories/', views.get_categories),
    path('get_quiz/', views.get_quiz),
]
