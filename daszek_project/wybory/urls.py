from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.GminyView.as_view(), name='gminy'),
	url(r'^(?P<nazwa_gminy>.+)/$', views.obwody, name='obwody'),
	url(r'^(?P<nazwa_gminy>.+)/zmiana$', views.zmiana, name='zmiana'),
	url(r'^(?P<nazwa_gminy>.+)/zapytanie_ajax$', views.zapytanie_ajax, name='zapytanie_ajax'),
	url(r'^(?P<nazwa_gminy>.+)/zmiana_ajax$', views.zmiana_ajax, name='zmiana_ajax'),
#	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
#	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
