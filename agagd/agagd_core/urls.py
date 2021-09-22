# AGAGD Beta Imports
from agagd_core.views.beta.core import list_all_tournaments, tournament_detail
from agagd_core.views.beta.qualifications import QualificationsView
from agagd_core.views.beta.search import SearchView

# Django Imports
from django.urls import path

# Note: Based of request for single qoutes.
# fmt: off
beta_patterns = ([
        path('tournaments/', list_all_tournaments, name='tournaments_list'),
        path('tournaments/<slug:code>/', tournament_detail, name='tournament_detail'),
        path('qualifications/', QualificationsView.as_view(), name='qualifications_overview')
], 'beta')
