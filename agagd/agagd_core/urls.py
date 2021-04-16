from agagd_core.views import beta as agagd_beta_views
from django.urls import path

beta_urlpatterns = (
    [
        path("", agagd_beta_views.index, name="index"),
        path("players/", agagd_beta_views.list_all_players, name="players_list"),
    ],
    "beta",
)
