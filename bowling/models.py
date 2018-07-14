from django.db import models

class Game(models.Model):
	# gameId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	gameId = models.AutoField(primary_key=True)
	currentFrameIndex = models.IntegerField(default=0)
	currentThrowIndex = models.IntegerField(default=0)
	gameOver = models.BooleanField(default=False)


	@classmethod
	def create(cls, sender, instance):
		for i in range(10):
			frame = Frame(gameId = instance)
			instance.frames.add(frame, bulk=False)
		instance.save()

	def getFrames(self):
		return self.frames.all()

	def updateFrame(self, score):
		currentFrame = self.frames.all()[self.currentFrameIndex]
		currentFrame.updateScores(score)
		if currentFrame.finished():
			self.currentFrameIndex += 1	
		if self.currentFrameIndex > 9:
			self.gameOver = True

	def __str__(self):
		return "Game ID: {}".format(self.gameId)


class Frame(models.Model):
	gameId = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='frames', default=0)
	throwIndex = models.IntegerField(default=0, choices=[(i,i) for i in range(2)])
	firstThrow = models.IntegerField(default=0)
	secondThrow = models.IntegerField(default=0)
	isSpare = models.BooleanField(default=False)
	isStrike = models.BooleanField(default=False)
	isFinished = models.BooleanField(default=False)

	def updateScores(self, score):
		if self.throwIndex == 0:
			self.firstThrow = score
			if self.firstThrow == 10:
				self.isStrike = True
				self.isFinished = True
			self.throwIndex += 1
			self.save()
		elif self.throwIndex == 1:
			self.secondThrow = score
			if self.secondThrow == 10 - self.firstThrow:
				self.isSpare = True
			self.isFinished = True
			self.save()

	def getFirstThrow(self):
		return firstThrow

	def getSecondThrow(self):
		return secondThrow

	def finished(self):
		return isFinished

	def __str__(self):
		return "First Throw: {}, Second Throw: {}".format(self.firstThrow, self.secondThrow)
