from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Game, Frame
from .serializers import GameSerializer, FrameSerializer

class BaseViewTest(APITestCase):
	client = APIClient()

	@staticmethod
	def createGame():
		Game.objects.create()

	def setUp(self):
		self.createGame()
		self.createGame()
		self.createGame()


class GetAllGamesTest(BaseViewTest):
	def getAllGames(self):
		response = self.client.get(reverse('games_all'))

		expected = Game.objects.all()
		serialized = GameSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)