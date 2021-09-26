from agagd_core.views import core as agagd_views
from agagd_core.views.all_players import AllPlayersPageView
from agagd_core.views.all_tournaments import AllTournamentsPageView
from agagd_core.views.api import ApiStatusView
from agagd_core.views.index import FrontPageView
from agagd_core.views.players_profile import PlayersProfilePageView
from agagd_core.views.qualifications import QualificationsPageView
from agagd_core.views.ratings_overview import RatingsOverviewPageView
from agagd_core.views.search import SearchView
from agagd_core.views.tournament_detail import TournamentDetailPageView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path("", FrontPageView.as_view(), name="frontpage_view"),
    path("api/games/count/daily/", agagd_views.game_stats, name="game_stats"),
    path("api/status/", ApiStatusView.as_view(), name="api_status_view"),
    path(
        "api/ratings/<int:member_id>/",
        agagd_views.member_ratings,
        name="member_ratings",
    ),
    path("players/", AllPlayersPageView.as_view(), name="players_list"),
    path(
        "players/<int:player_id>/",
        PlayersProfilePageView.as_view(),
        name="players_profile",
    ),
    path(
        "ratings/overview/",
        RatingsOverviewPageView.as_view(),
        name="ratings_overview_page_view",
    ),
    path(
        "ratings/qualifications/",
        QualificationsPageView.as_view(),
        name="qualifications_page_view",
    ),
    path("search/", SearchView.as_view(), name="search"),
    path("search/q<str:query>/", SearchView.as_view(), name="search"),
    path(
        "tournaments/",
        AllTournamentsPageView.as_view(),
        name="all_tournaments_page_view",
    ),
    path(
        "tournaments/<slug:code>/",
        TournamentDetailPageView.as_view(),
        name="tournament_detail",
    ),
    url(r".php$", RedirectView.as_view(url=reverse_lazy("index"))),
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
]

# DebugToolbar URL Configuration
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
