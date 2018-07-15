from django.urls import path
from .views import ListGamesView, BowlingApiView, CreateNewGameView

urlpatterns = [
	path('games/', ListGamesView.as_view(), name='games_all'),
	path('games/create/', CreateNewGameView.as_view(), name='game_create'),
	path('games/<int:gameId>/', BowlingApiView.as_view(), name='game_detail'),
]