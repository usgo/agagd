# AGAGD Models Imports
import agagd_core.models as agagd_models

# AGAGD Django Tables Imports
from agagd_core.tables.beta import GamesTable, PlayersTournamentTable

# Django Imports
from django.db.models import Q
from django.shortcuts import render


def players_profile(request, player_id):
    player = agagd_models.Member.objects.get(member_id=player_id)

    player_games = agagd_models.Game.objects.filter(
        Q(pin_player_1__exact=player_id) | Q(pin_player_2__exact=player_id)
    ).order_by("-game_date")

    player_rating = agagd_models.Players.objects.filter(
        Q(pin_player__exact=player_id)
    ).values("pin_player", "rating", "sigma")

    return render(
        request,
        "beta.player_profile.html",
        {
            "player": player,
            # "tournaments_table": tournaments_table,
            # "opponents_table": opponents_table,
        },
    )
