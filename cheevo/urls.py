from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.input_username),
	url(r'^user/(?P<pk>[0-9]+)/$', views.user_games_list),
)