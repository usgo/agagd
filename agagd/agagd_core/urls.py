# AGAGD Beta Imports
from agagd_core.views.beta.core import (
    list_all_players,
    list_all_tournaments,
    tournament_detail,
)
from agagd_core.views.beta.index import frontpage
from agagd_core.views.beta.information import InformationView
from agagd_core.views.beta.players_profile import players_profile

# Django Imports
from django.urls import path

# Note: Based of request for single qoutes.
# fmt: off
beta_patterns = ([
        path('', frontpage, name='index'),
        path('players/', list_all_players, name='players_list'),
        path('players/<int:player_id>/', players_profile, name='players_profile'),
        path('information/', InformationView.as_view(), name='ratings_overview'),
        path('tournaments/', list_all_tournaments, name='tournaments_list'),
        path('tournaments/<slug:code>/', tournament_detail, name='tournament_detail')
    ], 'beta')
