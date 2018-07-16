from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Game, Frame
from .serializers import GameSerializer, FrameSerializer, GameSerializerNoFrames
from collections import OrderedDict
import json



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

	def test_lastFrameStrikeHasThreeThrows(self):
		for i in range(8): #fill in first 9 frames to get to last
			self.game.updateScores(4)
			self.game.updateScores(2)
		self.game.updateScores(10)
		self.game.updateScores(9)
		self.game.updateScores(0)
		self.assertEqual(self.game.frames.all()[0].throwIndex, 2)

	def test_updatesGameOver(self):
		for i in range(9): #fill in all frames
			self.game.updateScores(4)
			self.game.updateScores(2)
		self.assertEqual(self.game.gameOver, True)

#API
class BaseViewTest(APITestCase):
	client = APIClient()

	@staticmethod
	def createGame():
		newGame = Game.objects.create()
		newGame.initialiseFrames()

	def setUp(self):
		self.createGame()
		self.createGame()
		self.createGame()

	def test_getAllGames(self):
		response = self.client.get('/games/')

		expected = Game.objects.all()
		serialized = GameSerializerNoFrames(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_postUpdatesGame(self):
		response = self.client.post('/games/1/', json.dumps({'score': 3}), content_type="application/json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_postUpdatesScore(self):
		self.client.post('/games/1/', json.dumps({'score': 3}), content_type="application/json")
		self.client.post('/games/1/', json.dumps({'score': 4}), content_type="application/json")
		expected = OrderedDict([('firstThrow', 3), ('secondThrow', 4), ('isSpare', False), ('isStrike', False), ('totalScore', 7)])
		response = self.client.get('/games/1/')
		self.assertEqual(response.data['frames'][0], expected)

	def test_postUpdatesScoreAfterStrike(self):
		self.client.post('/games/1/', json.dumps({'score': 10}), content_type="application/json")
		self.client.post('/games/1/', json.dumps({'score': 5}), content_type="application/json")
		expected = OrderedDict([('firstThrow', 10), ('secondThrow', 0), ('isSpare', False), ('isStrike', True), ('totalScore', 15)])
		response = self.client.get('/games/1/')
		self.assertEqual(response.data['frames'][0], expected)

	def test_postUpdatesScoreAfterSpare(self):
		self.client.post('/games/1/', json.dumps({'score': 4}), content_type="application/json")
		self.client.post('/games/1/', json.dumps({'score': 6}), content_type="application/json")
		self.client.post('/games/1/', json.dumps({'score': 2}), content_type="application/json")
		self.client.post('/games/1/', json.dumps({'score': 3}), content_type="application/json")
		expected = OrderedDict([('firstThrow', 4), ('secondThrow', 6), ('isSpare', True), ('isStrike', False), ('totalScore', 12)])
		response = self.client.get('/games/1/')
		self.assertEqual(response.data['frames'][0], expected)

	def test_getNewGame(self):
		response = self.client.get('/games/create/')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_getSpecificGame(self):
		response = self.client.get('/games/1/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_throwsErrorForInvalidScore(self):
		response = self.client.post('/games/1/', json.dumps({'score': 45}), content_type="application/json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
