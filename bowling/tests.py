from django.test import TestCase
from django.urls import reverse
from mock import patch
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Game, Frame
from .serializers import GameSerializer, FrameSerializer



#MODELS
class FrameTest(TestCase):
	def setUp(self):
		self.frame = Frame.objects.create()

	def test_frameUpdatesScore(self):
		self.frame.updateScores(3)
		self.frame.updateScores(4)
		self.assertEqual(self.frame.firstThrow, 3)
		self.assertEqual(self.frame.secondThrow, 4)
		self.assertEqual(self.frame.totalScore, 7)

	def test_frameStrike(self):
		self.frame.updateScores(10)
		self.assertEqual(self.frame.isStrike, True)

	def test_frameSpare(self):
		self.frame.updateScores(4)
		self.frame.updateScores(6)
		self.assertEqual(self.frame.isSpare, True)


class GameTest(TestCase):
	def setUp(self):
		self.game = Game.objects.create()
		self.game.initialiseFrames()

	def test_framesInitialised(self):
		self.assertEqual(len(self.game.frames.all()), 10)

	def test_frameIndexUpdates(self):
		self.assertEqual(self.game.currentFrameIndex, 0)
		self.game.updateScores(10) #strike - should change index
		self.assertEqual(self.game.currentFrameIndex, 1)
		self.game.updateScores(10) #strike - should change index
		self.assertEqual(self.game.currentFrameIndex, 2)

	def test_throwIndexUpdates(self):
		self.assertEqual(self.game.currentThrowIndex, 0)
		self.game.updateScores(5) 
		self.assertEqual(self.game.currentThrowIndex, 1)
		self.game.updateScores(3) 
		self.assertEqual(self.game.currentThrowIndex, 2)

	def test_strikeFrameUpdatesScore(self):
		self.game.updateScores(10)
		self.game.updateScores(3)
		self.game.updateScores(6)
		self.assertEqual(self.game.frames.all()[0].totalScore, 19)
		self.assertEqual(self.game.currentScore, 28)

	def test_spareFrameUpdatesScore(self):
		self.game.updateScores(3)
		self.game.updateScores(7)
		self.assertEqual(self.game.lastSpareIndex, 0)
		self.game.updateScores(4)
		self.game.updateScores(2)
		self.assertEqual(self.game.frames.all()[0].totalScore, 14)
		self.assertEqual(self.game.currentScore, 20)

#API
class BaseViewTest(APITestCase):
	client = APIClient()

	@staticmethod
	def createGame():
		Game.objects.create()

	def setUp(self):
		self.createGame()
		self.createGame()
		self.createGame()

	def test_getAllGames(self):
		response = self.client.get('/games/')

		expected = Game.objects.all()
		serialized = GameSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_getNewGame(self):
		response = self.client.get('/games/create/')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
