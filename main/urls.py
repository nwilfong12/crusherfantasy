from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('leaderboard/', views.leaderboard),
    path("about/", views.about_feedback, name="about_feedback"),
]