from rest_framework import serializers
from .models import Frame, Game

class GameSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Game
		fields = ['gameId']

class FrameSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Frame
		fields = ['firstThrow', 'secondThrow', 'isSpare', 'isStrike']