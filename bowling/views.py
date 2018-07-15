from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import GameSerializer, FrameSerializer, NewGameSerializer
from .models import Game, Frame

class ListGamesView(generics.ListAPIView):
	queryset = Game.objects.all()
	serializer_class = GameSerializer
	def get(self, request):
		return Response(status=status.HTTP_200_OK)


class CreateNewGameView(APIView):
	#Create a new game
	def get(self, request):
		newGame = Game()
		newGame.save()
		newGame.initialiseFrames()
		return Response(NewGameSerializer(newGame).data, status=status.HTTP_201_CREATED)


class BowlingApiView(APIView):
	#Get a certain game
	def get(self, request, gameId):
		try:
			game = Game.objects.get(gameId=gameId)
			return Response(GameSerializer(game).data, status=status.HTTP_200_OK)
		except IndexError as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	#Update a game 
	def put(self, request, gameId, score):
		try:
			game = Game.objects.get(gameId=gameId)
			game.updateFrame(score)
			return Response(status=status.HTTP_200_OK)
		except IndexError as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)