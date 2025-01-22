from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_quiz_view, name='home_quiz'),
    path('quiz/<slug:slug>/', views.quiz_view, name='quiz_view'),
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
]
