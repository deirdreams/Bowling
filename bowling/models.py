from django.db import models

class Game(models.Model):
	# gameId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	gameId = models.AutoField(primary_key=True)
	currentFrameIndex = models.IntegerField(default=0)
	currentThrowIndex = models.IntegerField(default=0)
	gameOver = models.BooleanField(default=False)
	currentScore = models.IntegerField(default=0)


	# @classmethod
	# def create(cls, sender, instance):
	# 	for i in range(10):
	# 		frame = Frame(gameId = instance)
	# 		instance.frames.add(frame, bulk=False)
	# 	instance.save()

	def initialiseFrames(self):
		for i in range(10):
			frame = Frame(gameId = self)
			frame.save()
			self.frames.add(frame, bulk=False)
		self.save()

	def getFrames(self):
		return self.frames.all()

	#TODO: update with game logic
	def updateFrame(self, score):
		currentFrame = self.frames.all()[self.currentFrameIndex]
		if currentFrame.finished():
			self.currentFrameIndex += 1	
		if self.currentFrameIndex > 9:
			self.gameOver = True
		currentFrame.updateScores(score)
		self.save()

	#keep index of the frame with the strike
	def addStrikeFrame(self):
		strikeFrame = StrikeFrame(frameId=currentFrameIndex, gameId=self)
		self.strike_frame.add(strikeFrame, bulk=False)
		self.save()

	def __str__(self):
		return "Game ID: {}".format(self.gameId)


class Frame(models.Model):
	gameId = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='frames', default=0)
	throwIndex = models.IntegerField(default=0, choices=[(i,i) for i in range(2)])
	firstThrow = models.IntegerField(default=0)
	secondThrow = models.IntegerField(default=0)
	thirdThrow = models.IntegerField(default=0) #for the third throw in last frame
	totalScore = models.IntegerField(default=0)
	isSpare = models.BooleanField(default=False)
	isStrike = models.BooleanField(default=False)

	def updateScores(self, score):
		if self.throwIndex == 0:
			self.firstThrow = score
			if self.firstThrow == 10:
				self.isStrike = True
		elif self.throwIndex == 1:
			self.secondThrow = score
			if self.secondThrow == 10 - self.firstThrow:
				self.isSpare = True
		elif self.throwIndex == 2:
			self.thirdThrow = score

		self.throwIndex +=1
		self.updateTotalScore()
		self.save()

	def updateTotalScore(self):
		self.totalScore = self.firstThrow + self.secondThrow + self.thirdThrow

	def getFirstThrow(self):
		return self.firstThrow

	def getSecondThrow(self):
		return self.secondThrow

	def getThrowIndex(self):
		return self.throwIndex

	def __str__(self):
		return "First Throw: {}, Second Throw: {}".format(self.firstThrow, self.secondThrow)


#Keep index of the strikes
class StrikeFrame(models.Model):
	frameId = models.IntegerField(default=0)
	gameId = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='strike_frame', default=0)

