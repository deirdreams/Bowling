from rest_framework import serializers
from .models import Frame, Game

class FrameSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Frame
		fields = ['firstThrow', 'secondThrow', 'isSpare', 'isStrike', 'totalScore']

class NewGameSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Game
		fields = ['gameId']

class GameSerializer(serializers.HyperlinkedModelSerializer):
	frames = FrameSerializer(many=True)
	class Meta:
		model = Game
		fields = ['gameId', 'currentScore', 'frames']