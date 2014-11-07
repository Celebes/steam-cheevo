from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.input_username),
	url(r'^user/(?P<pk>[0-9]+)/$', views.user_games_list),
	url(r'^games/$', views.all_games_list),
	url(r'^games/reload/games/$', views.reload_all_games, name='reload_all_games'),
	url(r'^games/reload/apps-are-games/$', views.check_if_apps_are_games, name='check_if_apps_are_games'),
	url(r'^games/reload/achievements/$', views.reload_all_achievements, name='reload_all_achievements'),
	url(r'^games/reload/difficulties/$', views.recalculate_difficulties, name='recalculate_difficulties'),
)