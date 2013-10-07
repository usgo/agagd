from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', 'agagd_core.views.index', name='index'),
    url(r'.php$', RedirectView.as_view(url=reverse_lazy('index'))),

    url(r'^search/$', 'agagd_core.views.search', name='search'),
    url(r'^player/(?P<member_id>\d+)/$', 'agagd_core.views.member_detail', name='member_detail'),
    url(r'^player/(?P<member_id>\d+)/vs/$', 'agagd_core.views.find_member_vs', name='find_member_vs'), 
    url(r'^player/(?P<member_id>\d+)/vs/(?P<other_id>\d+)$', 'agagd_core.views.member_vs', name='member_vs'), 

    url(r'^ratings/(?P<member_id>\d+)/$', 'agagd_core.views.member_ratings'), 

    url(r'^tournaments/$', 'agagd_core.views.tournament_list'),
    url(r'^tournaments/(?P<tourn_code>\w{1,20})/$', 'agagd_core.views.tournament_detail'),
)
