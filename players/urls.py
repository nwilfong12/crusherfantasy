from django.urls import path
from . import views

urlpatterns = [
    path("", views.players_list, name="players_list"),
path("player-search/", views.player_search, name="player_search"),
]