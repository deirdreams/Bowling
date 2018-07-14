from django.urls import path
from .views import ListGamesView

urlpatterns = [
	path('games/', ListGamesView.as_view(), name='games_all')
]