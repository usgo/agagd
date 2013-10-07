from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin 
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'agagd_core.views.index', name='index'),
    url(r'.php$', RedirectView.as_view(url=reverse_lazy('index'))),

    url(r'^search/$', 'agagd_core.views.search', name='search'),
    url(r'^player/(?P<member_id>\d+)/$', 'agagd_core.views.member_detail'),
    url(r'^player/(?P<member_id>\d+)/vs/(?P<other_id>\d+)$', 'agagd_core.views.member_vs'), 

    url(r'^ratings/(?P<member_id>\d+)/$', 'agagd_core.views.member_ratings'), 
    url(r'^gamestats/$', 'agagd_core.views.game_stats'), 

    url(r'^tournaments/$', 'agagd_core.views.tournament_list'),
    url(r'^tournaments/(?P<tourn_code>\w{1,20})/$', 'agagd_core.views.tournament_detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

from django.conf import settings
if settings.ADMIN_ENABLED:
    urlpatterns += patterns(
        url(r'^admin/', include(admin.site.urls)),
        )

