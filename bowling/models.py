from django.db import models

class Game(models.Model):
	gameId = models.AutoField(primary_key=True)
	currentFrameIndex = models.IntegerField(default=0)
	currentThrowIndex = models.IntegerField(default=0) #keep track of the num throws for purposes of strikes
	gameOver = models.BooleanField(default=False)
	currentScore = models.IntegerField(default=0)
	lastSpareIndex = models.IntegerField(default=-1)

	def initialiseFrames(self):
		for i in range(10):
			frame = Frame(gameId = self)
			frame.save()
			self.frames.add(frame, bulk=False)
		self.save()

	def getFrames(self):
		return self.frames.all()

	def updateScores(self, score):
		currentFrame = self.frames.all()[self.currentFrameIndex]
		if not self.checkValidScore(score, currentFrame):
			raise ValueError("Score is invalid.")

		if self.gameOver:
			raise ValueError("This game is over.")

		currentFrame.updateScores(score)
		self.currentScore += score
		#Update previous frames if they were strikes/spares
		if self.currentFrameIndex != 9:
			self.handlePrevStrikes(score)
			self.handlePrevSpares(score)

		if score == 10:
			self.addStrikeFrame()

		if currentFrame.isSpare:
			self.lastSpareIndex = self.currentFrameIndex

		#Change current frame index if necessary
		if (score == 10 or currentFrame.throwIndex > 1) and (self.currentFrameIndex != 9):
			self.currentFrameIndex += 1	

		self.currentThrowIndex += 1
		self.gameOver = self.checkGameOver(currentFrame)
		self.save()

	def checkGameOver(self, currentFrame):
		if self.currentFrameIndex < 9:
			return False
		frameStrikeOrSpare = (currentFrame.isSpare or currentFrame.isStrike) and currentFrame.throwIndex > 2
		frameNormal =  (not(currentFrame.isSpare and currentFrame.isStrike)) and currentFrame.throwIndex > 1
		return frameStrikeOrSpare or frameNormal


	def checkValidScore(self, score, frame):
		if score > 10 or (score > 10-frame.totalScore):
			return False
		else:
			return True

	def handlePrevStrikes(self, score):
		strikes = self.strike_frame.all()
		if len(strikes) == 0:
			return
		#loop through strikes and update score to previous frames if necessary
		for strike in strikes:
			if abs(self.currentThrowIndex - strike.frameId) < 3:
				self.frames.all()[strike.frameId].updateAddScore(score)
				self.currentScore += score
		self.save()

	def handlePrevSpares(self, score):
		if self.lastSpareIndex == -1: return
		self.frames.all()[self.lastSpareIndex].updateAddScore(score)
		self.currentScore += score
		self.lastSpareIndex = -1
		self.save()

	#keep index of the frame with the strike
	def addStrikeFrame(self):
		strikeFrame = StrikeFrame(frameId=self.currentFrameIndex, gameId=self)
		self.strike_frame.add(strikeFrame, bulk=False)
		self.save()

	def __str__(self):
		return "Game ID: {}".format(self.gameId)


class Frame(models.Model):
	gameId = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='frames', default=0)
	throwIndex = models.IntegerField(default=0, choices=[(i,i) for i in range(3)])
	firstThrow = models.IntegerField(default=0)
	secondThrow = models.IntegerField(default=0)
	thirdThrow = models.IntegerField(default=0) #for the third throw in last frame
	addScore = models.IntegerField(default=0) #additional score added for strike/spare
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

	def updateAddScore(self, score):
		self.addScore += score
		self.updateTotalScore()
		self.save()

	def updateTotalScore(self):
		self.totalScore = self.firstThrow + self.secondThrow + self.thirdThrow + self.addScore
		self.save()

	def __str__(self):
		return "First Throw: {}, Second Throw: {}".format(self.firstThrow, self.secondThrow)


#Keep index of the strikes
class StrikeFrame(models.Model):
	frameId = models.IntegerField(default=0)
	gameId = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='strike_frame', default=0)

