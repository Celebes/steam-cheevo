from django.db import models
from django.utils import timezone

class SteamUser(models.Model):
	nickname = models.CharField(max_length=255)
	steam_id = models.CharField(max_length=50, default='0')
	avatarfull = models.CharField(max_length=255, default='0')
	latest_refresh_date = models.DateTimeField(default=timezone.now)
	
	def refresh(self):
		self.latest_refresh_date = timezone.now()
		self.save()
		
	def __str__(self):
		return self.nickname

class SteamGame(models.Model):
	owners = models.ManyToManyField(SteamUser)
	
	has_achievements = models.BooleanField(default=False)
	is_game = models.BooleanField(default=True)
	
	appid = models.IntegerField()
	title = models.CharField(max_length=255)
	img_icon_url = models.CharField(max_length=255, default='0')
	difficulty_score = models.FloatField(default=0.0)
	
	def __str__(self):
		return self.title + " owned by " + owner
		
class GameAchievement(models.Model):
	game = models.ForeignKey(SteamGame)
	
	name = models.CharField(max_length=255, default='noname')
	percentage_of_people_that_unlocked = models.FloatField(default=0.0)
	
class GlobalStats(models.Model):
	last_database_update = models.DateTimeField(default=timezone.now)