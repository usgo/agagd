from django.urls import path
from agagd_core.views import beta as agagd_beta_views

# Note: Based of request for single qoutes.
# fmt: off
beta_patterns = ([
    path('', agagd_beta_views.index, name='index'),
    path('players/', agagd_beta_views.list_all_players, name='players_list'),
], 'beta')
