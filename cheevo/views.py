import requests
import time
import logging
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from .forms import UsernameForm
from .models import SteamUser, SteamGame, GameAchievement

steam_api_key = 'FAA78102E0EEFF52D4F96CC1F4497EA7'
steam_nick_to_id_url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
steam_owned_games_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
steam_player_info_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
steam_all_games_url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
steam_ach_percent_url = 'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/'
steam_game_details_url = 'http://store.steampowered.com/api/appdetails/'

# logging
now = datetime.datetime.now()
log_file_name = './logs/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second) + '.log'

logging.basicConfig(filename=log_file_name, level=logging.INFO)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

logger = logging.getLogger(__name__)

def input_username(request):
	if request.method == "POST":
		form = UsernameForm(request.POST)
		if form.is_valid():
			# utworz usera lub pobierz istniejacego z bazy danych
			inputted_nickname = form.cleaned_data['nickname']
			if not SteamUser.objects.filter(nickname=inputted_nickname):
			
				# pobierz ID usera ze steam API na podstawie nicku
				nick_to_id_params = {'key': steam_api_key, 'vanityurl': inputted_nickname}
				nick_to_id_result = requests.get(steam_nick_to_id_url, params=nick_to_id_params)
				
				if nick_to_id_result.json()['response']['success'] == 1:
					user_steam_id = nick_to_id_result.json()['response']['steamid']
					logger.info('user ID = ' + user_steam_id)
					
					player_info_params = {'key': steam_api_key, 'steamids': user_steam_id}
					player_info_result = force_connection(steam_player_info_url, player_info_params)
					
					steam_user = form.save(commit=False)
					steam_user.steam_id = user_steam_id
					steam_user.avatarfull = player_info_result.json()['response']['players'][0]['avatarfull']
					steam_user.save()
				else:
					logger.info('user ID not found')
				
			else:
				steam_user = SteamUser.objects.filter(nickname=inputted_nickname)[:1].get()			
			
			return redirect('cheevo.views.user_games_list', pk=steam_user.pk)
	else:
		form = UsernameForm()
		
	# ilosc osiagniec i gier w bazie do wyswietlenia na stronce
	games_count = str(len(list(SteamGame.objects.filter(is_game=True, has_achievements=True))))
	achievements_count = str(len(list(GameAchievement.objects.all())))
	
	return render(request, 'cheevo/input_username.html', {'form': form, 'games_count': games_count, 'achievements_count': achievements_count})
	
def user_games_list(request, pk):
	steam_user = get_object_or_404(SteamUser, pk=pk)
	
	time_now = timezone.now()
	time_diff = time_now - steam_user.latest_refresh_date
	
	if time_diff.total_seconds() >= 1:
		logger.info('odswiezono liste gier uzytkownika!')
		steam_user.refresh()
	
		steam_owned_games_params = {'key': steam_api_key, 'steamid': steam_user.steam_id, 'format': 'json', 'include_appinfo': '1'}
		steam_owned_games_result = force_connection(steam_owned_games_url, steam_owned_games_params)
		
		owned_games_list = steam_owned_games_result.json()['response']['games']
		
		for game in owned_games_list:
			# jesli nie ma takiej gry w bazie to ja pomin
			if not SteamGame.objects.filter(appid=game['appid']):
				continue
			
			game_in_db = SteamGame.objects.filter(appid=game['appid'])[:1].get()
			
			# jesli gra nie ma ikonki to ja dodaj
			if game_in_db.img_icon_url == '0':
				game_in_db.img_icon_url = game['img_icon_url']
			
			# jesli gracz nie ma przypisanej danej gry to ja przypisz
			if steam_user not in game_in_db.owners.all():
				game_in_db.owners.add(steam_user)
			
			# zapisz gre
			game_in_db.save()		
	else:
		logger.info('jeszcze tylko' + str(3600 - int(time_diff.total_seconds())) + ' sekund do mozliwosci odswiezenia')
		
	owned_games_list_from_db = list(SteamGame.objects.filter(owners__steam_id=steam_user.steam_id, is_game=True, has_achievements=True).order_by('-difficulty_score'))
	
	minutes = time_diff.total_seconds() / 60

	return render(request, 'cheevo/user_games_list.html', {'steam_user': steam_user, 'games': owned_games_list_from_db, 'minutes': minutes})

@login_required	
def all_games_list(request):
	games = SteamGame.objects.all()
	return render(request, 'cheevo/all_games_list.html', {'games': games})
	
def reload_all_games(request):
	logger.info('reloading all games!')

	steam_all_games_params = {'key': steam_api_key, 'format': 'json', 'include_appinfo': '1'}
	steam_all_games_result = force_connection(steam_all_games_url, steam_all_games_params)
		
	all_games_list = steam_all_games_result.json()['applist']['apps']
	
	logger.info('number of games before: ' + str(len(SteamGame.objects.all())))
	
	for game in all_games_list:
		if not SteamGame.objects.filter(appid=game['appid']):
			steamGame = SteamGame()
			steamGame.appid = game['appid']
			steamGame.title = game['name']
			steamGame.save()
	
	logger.info('number of games after: ' + str(len(SteamGame.objects.all())))
	
	return redirect('cheevo.views.all_games_list')

# ta metoda teraz sprawdza tylko czy dane appid jest typu game lub dlc
def check_if_apps_are_games(request):
	logger.info('checking if games have achievements')
	
	# pobierz liste gier z bd
	all_games_from_db = list(SteamGame.objects.all().order_by('appid'))
	all_games_len = str(len(all_games_from_db))
	counter = 0
	
	for steamGame in all_games_from_db:
		counter += 1
		logger.info('sprawdzanie czy appka [' + str(counter) + '/' + all_games_len + '] o appid = ' + str(steamGame.appid) + ' jest gra')
		
		if steamGame.is_game == False:
			logger.info('BEZ POLACZENIA Z API - to nie gra!')
			continue

		is_success = False	
		
		try:
			while True:
				try:
					steam_game_details_params = {'key': steam_api_key, 'appids': steamGame.appid, 'format': 'json'}
					steam_game_details_result = force_connection(steam_game_details_url, steam_game_details_params)
					
					is_success = steam_game_details_result.json()[str(steamGame.appid)]['success']
					app_type = steam_game_details_result.json()[str(steamGame.appid)]['data']['type']
				except ValueError:
					logger.error('value error!')
					logger.error(steam_game_details_result.text)
					time.sleep(1)
					continue
				break
				
			if is_success == True:
				if app_type != 'game' and app_type != 'dlc':
					logger.info('to nie gra!')
					steamGame.is_game = False
					steamGame.save()
					continue
				else:
					logger.info('to jest gra lub dlc!')
		except KeyError:
			logger.error('KeyError!')
			steamGame.is_game = False
			steamGame.save()
			continue
				
		if is_success == False:
			steamGame.is_game = False
			steamGame.save()
			logger.info('success FALSE!')
			continue

	logger.info('koniec sprawdzanie ktore z gier to gry lub dlc!')
	return redirect('cheevo.views.all_games_list')
	
def reload_all_achievements(request):
	logger.info('reload user games achievements!')
	
	# pobierz liste gier z bd
	all_games_from_db = list(SteamGame.objects.all().order_by('appid'))
	all_games_len = str(len(all_games_from_db))
	counter = 0
	
	for steamGame in all_games_from_db:
		counter += 1		
		logger.info('pobieranie osiagniec dla gry [' + str(counter) + '/' + all_games_len + '] o appid = ' + str(steamGame.appid) + '...')
		
		if steamGame.is_game == False:
			logger.info('to nie gra!')
			continue

		try:
			# pobierz z api globalne statystyki osiagniec dla danej gry
			while True:
				try:
					steam_ach_percent_params = {'key': steam_api_key, 'gameid': steamGame.appid, 'format': 'json'}
					steam_ach_percent_result = force_connection(steam_ach_percent_url, steam_ach_percent_params)
					
					list_of_achievements = steam_ach_percent_result.json()['achievementpercentages']['achievements']
				except ValueError:
					logger.error('value error!')
					logger.error(steam_ach_percent_result.text)
					time.sleep(1)
					continue
				break
		
			# przypisz osiagniecia do gier, o ile juz nie sa przypisane i jesli gra ma osiagniecia
			if list_of_achievements:
				for achievement in list_of_achievements:
					if not GameAchievement.objects.filter(game=steamGame, name=achievement['name']):
						newAchievement = GameAchievement()
						newAchievement.game = steamGame
						newAchievement.name = achievement['name']
						newAchievement.percentage_of_people_that_unlocked = achievement['percent']
						newAchievement.save()
					else:
						existingAchievement = GameAchievement.objects.filter(game=steamGame, name=achievement['name'])[:1].get()
						existingAchievement.percentage_of_people_that_unlocked = achievement['percent']
						existingAchievement.save()
				
				steamGame.has_achievements = True
				steamGame.save()
					
				logger.info('pomyslnie pobrano ' + str(len(steam_ach_percent_result.json()['achievementpercentages']['achievements'])) + ' osiagniec dla gry o appid = ' + str(steamGame.appid))
			else:
				logger.info('brak osiagniec dla gry o appid = ' + str(steamGame.appid))
		except KeyError:
			logger.info('brak osiagniec dla tej gry o appid = ' + str(steamGame.appid))
			continue
	logger.info('pomyslnie zaktualizowano osiagniecia dla ' + all_games_len + ' gier')
	return redirect('cheevo.views.all_games_list')
	
def recalculate_difficulties(request):
	logger.info('recalculate difficulties!')
	
	# pobierz liste gier z bd
	all_games_from_db = list(SteamGame.objects.all().order_by('appid'))
	all_games_len = str(len(all_games_from_db))
	counter = 0
	
	for steamGame in all_games_from_db:
		counter += 1
		logger.info('obliczanie trudnosci gry o appid = ' + str(steamGame.appid) + '...')
		
		if steamGame.is_game == False:
			logger.info('to nie gra!')
			continue
			
		if steamGame.has_achievements == False:
			logger.info('ta gra nie ma osiagniec!')
			continue
			
		steamGameAchievements = GameAchievement.objects.filter(game=steamGame)
		
		if not steamGameAchievements:
			logger.info('brak achievementow')
			continue
		
		percentagesList = []
		numberOfAchievementsBelowOne = 0
		try:
			minPercent = 100
			
			for achievement in steamGameAchievements:
				currentPercent = float(achievement.percentage_of_people_that_unlocked)
				
				if not 0.01 <= currentPercent <= 100:
					continue
				
				if currentPercent < 1:
					numberOfAchievementsBelowOne += 1
				
				percentagesList.append(currentPercent)
				
				if currentPercent < minPercent:
					minPercent = currentPercent
			
			steamGame.difficulty_score = minPercent
			
			if numberOfAchievementsBelowOne > 0:
				steamGame.difficulty_score /= numberOfAchievementsBelowOne
			
			steamGame.save()
			
			logger.info('[' + str(steamGame.appid) + '] Znaleziono ' + str(len(percentagesList)) + ' osiagniec, najtrudniejsze z nich zdobylo ' + str(minPercent) + ' % graczy, trudnosc gry = ' + str(steamGame.difficulty_score))
		except GameAchievement.DoesNotExist:
			logger.info('brak osiagniec w bazie, mimo, ze gra miala kategorie 22 = ' + str(steamGame.appid))
		
	logger.info('zakonczono przeliczanie trudnosci gier')
	return redirect('cheevo.views.all_games_list')
	
def force_connection(url, url_params):
	result = None
	
	while True:
		try:
			result = requests.get(url, params=url_params)
		except requests.ConnectionError:
			logger.error('blad polaczenia! wznawiam operacje')
			continue
		break
	return result