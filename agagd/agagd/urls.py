from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', 'agagd_core.views.index', name='index'),
    url(r'.php$', RedirectView.as_view(url=reverse_lazy('index'))),

    url(r'^search/$', 'agagd_core.views.search', name='search'),
    url(r'^player/(?P<member_id>\d+)/$', 'agagd_core.views.member_detail', name='member_detail'),
    url(r'^chapter/(?P<chapter_code>\w+)/$', 'agagd_core.views.chapter_detail', name='chapter_detail'),
    url(r'^country/(?P<country_name>[\w ]+)/$', 'agagd_core.views.country_detail', name='country_detail'),
    url(r'^player/(?P<member_id>\d+)/vs/$', 'agagd_core.views.find_member_vs', name='find_member_vs'), 
    url(r'^player/(?P<member_id>\d+)/vs/(?P<other_id>\d+)$', 'agagd_core.views.member_vs', name='member_vs'), 

    url(r'^ratings/(?P<member_id>\d+)/$', 'agagd_core.views.member_ratings'), 
    url(r'^gamestats/$', 'agagd_core.views.game_stats'), 

    url(r'^tournaments/$', 'agagd_core.views.tournament_list', name='tourney_list'),
    url(r'^tournaments/(?P<tourn_code>\w{1,20})/$', 'agagd_core.views.tournament_detail'),

    # Static Pages
    url(r'^information/$', 'agagd_core.views.information', name='information'),
    url(r'^qualifications/$', 'agagd_core.views.qualifications', name='qualifications')
)
