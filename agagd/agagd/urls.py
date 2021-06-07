from agagd_core import urls as beta_urls
from agagd_core.views import core as agagd_views
from agagd_core.views.core import InformationPageView, QualificationsPageView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r"^$", agagd_views.index, name="index"),
    url(r".php$", RedirectView.as_view(url=reverse_lazy("index"))),
    url(r"^search/$", agagd_views.search, name="search"),
    url(
        r"^player/(?P<member_id>\d+)/$", agagd_views.member_detail, name="member_detail"
    ),
    url(
        r"^chapter/(?P<chapter_id>\d+)/$",
        agagd_views.chapter_detail,
        name="chapter_detail",
    ),
    url(
        r"^chapter/(?P<chapter_code>\w+)/$",
        agagd_views.chapter_code_redirect,
        name="chapter_code_redirect",
    ),
    url(
        r"^country/(?P<country_name>[\w ]+)/$",
        agagd_views.country_detail,
        name="country_detail",
    ),
    url(
        r"^player/(?P<member_id>\d+)/vs/$",
        agagd_views.find_member_vs,
        name="find_member_vs",
    ),
    url(
        r"^player/(?P<member_id>\d+)/vs/(?P<other_id>\d+)$",
        agagd_views.member_vs,
        name="member_vs",
    ),
    url(
        r"^all_player_ratings/$",
        agagd_views.all_player_ratings,
        name="all_player_ratings",
    ),
    url(
        r"^ratings/(?P<member_id>\d+)/$",
        agagd_views.member_ratings,
        name="member_ratings",
    ),
    url(r"^gamestats/$", agagd_views.game_stats, name="game_stats"),
    url(r"^tournaments/$", agagd_views.tournament_list, name="tourney_list"),
    url(
        r"^tournaments/(?P<tourn_code>\w{1,20})/$",
        agagd_views.tournament_detail,
        name="tournament_detail",
    ),
    # Pages
    path("information/", InformationPageView.as_view()),
    path("qualifications/", QualificationsPageView.as_view()),
    # Beta
    path("beta/", include(beta_urls.beta_patterns)),
]

# DebugToolbar URL Configuration
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
