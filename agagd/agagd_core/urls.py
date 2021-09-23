# AGAGD Beta Imports
from agagd_core.views.beta.core import tournament_detail

# Django Imports
from django.urls import path

# Note: Based of request for single qoutes.
# fmt: off
beta_patterns = ([
        path('tournaments/<slug:code>/', tournament_detail, name='tournament_detail'),
], 'beta')
