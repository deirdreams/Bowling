from django.shortcuts import render
from rest_framework import generics
from .serializers import GameSerializer, FrameSerializer
from .models import Game, Frame

class ListGamesView(generics.ListAPIView):
	queryset = Game.objects.all()
	serializer_class = GameSerializer

	