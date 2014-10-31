from django.db import models
from django.utils import timezone

class SteamUser(models.Model):
	nickname = models.CharField(max_length=255)
	#profile_image
	latest_refresh_date = models.DateTimeField(default=timezone.now)
	
	def refresh(self):
		self.latest_refresh_date = timezone.now()
		self.save()
		
	def __str__(self):
		return self.nickname

class SteamGame(models.Model):
	owner = models.ForeignKey(SteamUser)
	
	title = models.CharField(max_length=255)
	#game_image
	hours_played = models.FloatField(default=0.0)
	difficulty_score = models.FloatField(default=0.0)
	
	def __str__(self):
		return self.title + " owned by " + owner
		
class GameAchievement(models.Model):
	game = models.ForeignKey(SteamGame)
	
	name = models.CharField(max_length=255)
	#achievement_image
	unlocked = models.BooleanField(default=False)
	percentage_of_people_that_unlocked = models.FloatField(default=0.0)