# AGAGD Beta Imports
from agagd_core.views.beta.core import (
    list_all_players,
    list_all_tournaments,
    player_profile,
    tournament_detail,
)
from agagd_core.views.beta.index import frontpage

# Django Imports
from django.urls import path

# Note: Based of request for single qoutes.
# fmt: off
beta_patterns = ([
        path('', frontpage, name='index'),
        path('players/', list_all_players, name='players_list'),
        path('players/<int:player_id>/', player_profile, name='player_profile'),
        path('tournaments/', list_all_tournaments, name='tournaments_list'),
        path('tournaments/<slug:code>/', tournament_detail, name='tournament_detail')
    ], 'beta')
