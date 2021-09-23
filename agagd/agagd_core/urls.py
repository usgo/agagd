# AGAGD Beta Imports
from agagd_core.views.beta.core import tournament_detail
from agagd_core.views.beta.qualifications import QualificationsView

# Django Imports
from django.urls import path

# Note: Based of request for single qoutes.
# fmt: off
beta_patterns = ([
        path('tournaments/<slug:code>/', tournament_detail, name='tournament_detail'),
        path('qualifications/', QualificationsView.as_view(), name='qualifications_overview')
], 'beta')
