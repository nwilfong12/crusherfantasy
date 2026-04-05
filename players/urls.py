from django.urls import path
from . import views
from .views import trade_calculator, player_search, evaluate_trade_api
urlpatterns = [
    path("", views.players_list, name="players_list"),
    path("player-search/", views.player_search, name="player_search"),
path("trade/", trade_calculator, name="trade_calculator"),
path("search/", player_search, name="player_search"),
    path("evaluate/", evaluate_trade_api),
]