from agagd_core.views import beta
from django.urls import path

# Note: Based of request for single qoutes.
# fmt: off
beta_patterns = ([
        path('', beta.index, name='index'),
        path('players/', beta.list_all_players, name='players_list'),
        path('players/<int:player_id', beta.player_profile, name='player_profile'),
        path('tournaments/', beta.list_all_tournaments, name='tournaments_list'),
        path('tournaments/<slug:code>/', beta.tournament_detail, name='tournament_detail')
    ], 'beta')
