from agagd_core.views import beta
from django.urls import path

# Note: Based of request for single qoutes.
# fmt: off
beta_patterns = ([
        path('', beta.index, name='index'),
        path('players/', beta.list_all_players, name='players_list'),
    ], 'beta')
