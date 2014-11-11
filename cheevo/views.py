import requests
import time
import logging
import datetime
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from .forms import UsernameForm
from .models import SteamUser, SteamGame, GameAchievement, GlobalStats

steam_api_key = '23260ACA5F93979697902D234A95E06C'
steam_nick_to_id_url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
steam_owned_games_url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
steam_player_info_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
steam_all_games_url = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
steam_ach_percent_url = 'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/'
steam_game_details_url = 'http://store.steampowered.com/api/appdetails/'

logger = logging.getLogger(__name__)

def input_username(request):
	username_error = False
	inputted_nickname = ""
	
	if request.method == "POST":
		form = UsernameForm(request.POST)
		if form.is_valid():
			# utworz usera lub pobierz istniejacego z bazy danych
			inputted_nickname = form.cleaned_data['nickname']
			
			regexp = re.compile(r'^[0-9]*$')
			reg_match = False
			new_user = False
			
			if regexp.match(inputted_nickname) is not None:
				print('wpisano ID!')
				reg_match = True
				if not SteamUser.objects.filter(steam_id=inputted_nickname):
					user_steam_id = inputted_nickname
					new_user = True
				else:
					steam_user = SteamUser.objects.filter(steam_id=inputted_nickname)[:1].get()
				
			else:
				if not SteamUser.objects.filter(nickname=inputted_nickname):
					# pobierz ID usera ze steam API na podstawie nicku
					nick_to_id_params = {'key': steam_api_key, 'vanityurl': inputted_nickname}
					nick_to_id_result = force_connection(steam_nick_to_id_url, nick_to_id_params)
					
					if nick_to_id_result.json()['response']['success'] == 1:
						user_steam_id = nick_to_id_result.json()['response']['steamid']
						new_user = True
						logger.info('user ID = ' + user_steam_id)
					else:
						logger.error('user ID not found - ' + inputted_nickname)
						
				else:
					steam_user = SteamUser.objects.filter(nickname=inputted_nickname)[:1].get()
			
			if new_user == True:
				player_info_params = {'key': steam_api_key, 'steamids': user_steam_id}
				player_info_result = force_connection(steam_player_info_url, player_info_params)
				
				steam_user = form.save(commit=False)
				
				if reg_match == True:
					steam_user.personaname = player_info_result.json()['response']['players'][0]['personaname']
				else:
					steam_user.personaname = inputted_nickname
				
				steam_user.steam_id = user_steam_id
				steam_user.avatarfull = player_info_result.json()['response']['players'][0]['avatarfull']
				steam_user.save()
			
			try:
				return redirect('cheevo.views.user_games_list', pk=steam_user.pk)
			except UnboundLocalError:
				username_error = True
		else:
			logger.error('user ID not valid')
	else:
		form = UsernameForm()
		
	# ilosc osiagniec i gier w bazie do wyswietlenia na stronce
	games_count = str(len(list(SteamGame.objects.filter(has_achievements=True))))
	achievements_count = str(len(list(GameAchievement.objects.all())))
	
	try:
		last_update = GlobalStats.objects.latest('id').last_database_update
		str_last_update = last_update.strftime("%d-%m-%Y")
	except GlobalStats.DoesNotExist:
		str_last_update = 'Never.'

	return render(request, 'cheevo/input_username.html', {'form': form, 'games_count': games_count, 'achievements_count': achievements_count, 'str_last_update': str_last_update, 'username_error': username_error, 'inputted_nickname': inputted_nickname})
	
def user_games_list(request, pk):
	steam_user = get_object_or_404(SteamUser, pk=pk)
	logger.info('zaladowano liste gier dla uzytkownika: ' + steam_user.nickname)
	
	minutes = 0
	
	if not steam_user.latest_refresh_date == None:
		time_diff = timezone.now() - steam_user.latest_refresh_date
	
	if steam_user.latest_refresh_date == None or time_diff.total_seconds() >= 3600:
		logger.info('odswiezono liste gier uzytkownika!')
		steam_user.refresh()
		time_diff = timezone.now() - steam_user.latest_refresh_date
	
		steam_owned_games_params = {'key': steam_api_key, 'steamid': steam_user.steam_id, 'format': 'json', 'include_appinfo': '1'}
		steam_owned_games_result = force_connection(steam_owned_games_url, steam_owned_games_params)
		
		try:
			owned_games_list = steam_owned_games_result.json()['response']['games']
		except KeyError:
			owned_games_list = []
		
		if owned_games_list:
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
		logger.info('jeszcze tylko ' + str(3600 - int(time_diff.total_seconds())) + ' sekund do mozliwosci odswiezenia')
	
	if not steam_user.latest_refresh_date == None:
		minutes = time_diff.total_seconds() / 60
		
	owned_games_list_from_db = list(SteamGame.objects.filter(owners__steam_id=steam_user.steam_id, has_achievements=True).order_by('-difficulty_score'))

	return render(request, 'cheevo/user_games_list.html', {'steam_user': steam_user, 'games': owned_games_list_from_db, 'minutes': minutes})

@login_required	
def all_games_list(request):
	games = SteamGame.objects.all()
	return render(request, 'cheevo/all_games_list.html', {'games': games})

@login_required	
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

@login_required	
def check_if_apps_are_games(request):
	logger.info('checking if games have achievements')
	
	# pobierz liste gier z bd
	all_games_from_db = list(SteamGame.objects.all().order_by('appid'))
	all_games_len = str(len(all_games_from_db))
	counter = 0
	
	for steamGame in all_games_from_db:
		counter += 1
		logger.info('sprawdzanie czy appka [' + str(counter) + '/' + all_games_len + '] o appid = ' + str(steamGame.appid) + ' jest gra')

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
					steamGame.delete()
					continue
				else:
					logger.info('to jest gra lub dlc!')
		except KeyError:
			logger.error('KeyError!')
			steamGame.delete()
			continue
				
		if is_success == False:
			steamGame.delete()
			logger.info('success FALSE!')
			continue
	
	logger.info('koniec sprawdzanie ktore z gier to gry lub dlc!')
	return redirect('cheevo.views.all_games_list')

@login_required	
def reload_all_achievements(request):
	logger.info('reload all achievements!')
	
	# pobierz liste gier z bd
	all_games_from_db = list(SteamGame.objects.all().order_by('appid'))
	all_games_len = str(len(all_games_from_db))
	counter = 0
	
	for steamGame in all_games_from_db:
		counter += 1		
		logger.info('pobieranie osiagniec dla gry [' + str(counter) + '/' + all_games_len + '] o appid = ' + str(steamGame.appid) + '...')

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
			
				min_ach = 100.0
				below_one_count = 0
				
				for achievement in list_of_achievements:
					curr_percent = float(achievement['percent'])
					
					if not 0.01 <= curr_percent <= 100:
						continue
						
					if curr_percent < min_ach:
						min_ach = curr_percent
						
					if curr_percent < 1:
						below_one_count += 1
				
				steamGame.min_achievement = min_ach
				steamGame.below_one_ach_count = below_one_count
				steamGame.has_achievements = True
				steamGame.save()
					
				logger.info('pomyslnie pobrano ' + str(len(steam_ach_percent_result.json()['achievementpercentages']['achievements'])) + ' osiagniec dla gry o appid = ' + str(steamGame.appid))
			else:
				logger.info('brak osiagniec dla gry o appid = ' + str(steamGame.appid))
				steamGame.delete()
		except KeyError:
			logger.info('brak osiagniec dla tej gry o appid = ' + str(steamGame.appid))
			steamGame.delete()
			continue
	logger.info('pomyslnie zaktualizowano osiagniecia dla ' + all_games_len + ' gier')
	return redirect('cheevo.views.all_games_list')

@login_required	
def recalculate_difficulties(request):
	logger.info('recalculate difficulties!')
	
	# pobierz liste gier z bd
	all_games_from_db = list(SteamGame.objects.all().order_by('appid'))
	all_games_len = str(len(all_games_from_db))
	counter = 0
	
	for steamGame in all_games_from_db:
		counter += 1
		logger.info('obliczanie trudnosci gry o appid = ' + str(steamGame.appid) + '...')
			
		if steamGame.has_achievements == False:
			logger.info('ta gra nie ma osiagniec!')
			continue
		
		steamGame.difficulty_score = steamGame.min_achievement
		
		if steamGame.below_one_ach_count > 1:
			steamGame.difficulty_score /= steamGame.below_one_ach_count
		
		steamGame.save()
		
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