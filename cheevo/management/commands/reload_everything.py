from django.core.management.base import BaseCommand, CommandError
import cheevo.views
from cheevo.models import GlobalStats
from django.utils import timezone

class Command(BaseCommand):
    help = 'Reloads everything in this order: downloads list of apps, determines which of them are games, loads achievements for games and finally recalculates difficulties'

    def handle(self, *args, **options):
        cheevo.views.logger.info('*******************************************************')
        cheevo.views.logger.info('* AUTOMATYCZNIE URUCHOMIONO KOMENDE RELOAD_EVERYTHING *')
        cheevo.views.logger.info('*******************************************************')
        
        cheevo.views.logger.info('')
        
        cheevo.views.logger.info('******************************************************')
        cheevo.views.logger.info('************ START POBIERANIA LISTY APPEK ************')
        cheevo.views.logger.info('******************************************************')
        
        cheevo.views.logger.info('')
        #cheevo.views.reload_all_games(None)
        cheevo.views.logger.info('')
        
        cheevo.views.logger.info('******************************************************')
        cheevo.views.logger.info('******** START SPRAWDZANIA KTORE APPKI TO GRY ********')
        cheevo.views.logger.info('******************************************************')
        
        cheevo.views.logger.info('')
        #cheevo.views.check_if_apps_are_games(None)
        cheevo.views.logger.info('')
        
        cheevo.views.logger.info('******************************************************')
        cheevo.views.logger.info('************* START POBIERANIA OSIAGNIEC *************')
        cheevo.views.logger.info('******************************************************')
        
        cheevo.views.logger.info('')
        #cheevo.views.reload_all_achievements(None)
        cheevo.views.logger.info('')
        
        cheevo.views.logger.info('******************************************************')
        cheevo.views.logger.info('******* START PRZELICZANIA TRUDNOSCI OSIAGNIEC *******')
        cheevo.views.logger.info('******************************************************')
        
        cheevo.views.logger.info('')
        #cheevo.views.recalculate_difficulties(None)
        cheevo.views.logger.info('')
        
        cheevo.views.logger.info('******************************************************')
        cheevo.views.logger.info('** ZAKONCZONO WYKONYWANIE KOMENDY RELOAD_EVERYTHING **')
        cheevo.views.logger.info('******************************************************')
        
        stats = GlobalStats()
        stats.last_database_update = timezone.now()
        stats.save()
		