from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from agagd_core import views as agagd_views

urlpatterns = [
    url(r'^$', agagd_views.index, name='index'),
    url(r'.php$', RedirectView.as_view(url=reverse_lazy('index'))),

    url(r'^search/$', agagd_views.search, name='search'),
    url(r'^player/(?P<member_id>\d+)/$', agagd_views.member_detail, name='member_detail'),
    url(r'^chapter/(?P<chapter_code>\w+)/$', agagd_views.chapter_detail, name='chapter_detail'),
    url(r'^country/(?P<country_name>[\w ]+)/$', agagd_views.country_detail, name='country_detail'),
    url(r'^player/(?P<member_id>\d+)/vs/$', agagd_views.find_member_vs, name='find_member_vs'),
    url(r'^player/(?P<member_id>\d+)/vs/(?P<other_id>\d+)$', agagd_views.member_vs, name='member_vs'),
    url(r'^all_player_ratings/$', agagd_views.all_player_ratings, name='all_player_ratings'),

    url(r'^ratings/(?P<member_id>\d+)/$', agagd_views.member_ratings, name='member_ratings'),
    url(r'^gamestats/$', agagd_views.game_stats, name='game_stats'),

    url(r'^tournaments/$', agagd_views.tournament_list, name='tourney_list'),
    url(r'^tournaments/(?P<tourn_code>\w{1,20})/$', agagd_views.tournament_detail, name='tournament_detail'),

    # Static Pages
    url(r'^information/$', agagd_views.information),
    url(r'^qualifications/$', agagd_views.qualifications)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
