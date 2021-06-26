# AGAGD Imports
import agagd_core.models as agagd_models

# Django Tables Imports
from agagd_core.tables.beta import (
    GamesTable,
    PlayersTournamentTable,
    Top10DanTable,
    Top10KyuTable,
    TournamentsTable,
)

# Django Imports
from django.shortcuts import render


def frontpage(request):
    latest_games = agagd_models.Game.objects.values(
        "game_date",
        "handicap",
        "pin_player_1",
        "pin_player_2",
        "tournament_code",
        "result",
    ).order_by("-game_date")[:25]

    latest_tournaments = agagd_models.Tournament.objects.all().order_by("-elab_date")[
        :25
    ]

    top_10_dan_kyu = agagd_models.Players.objects.values(
        "pin_player", "sigma", "rating"
    )

    top_10_dan = top_10_dan_kyu.filter(rating__gt=0).order_by("-rating")[:10]
    top_10_kyu = top_10_dan_kyu.filter(rating__lt=0).order_by("-rating")[:10]

    # Index Tables
    latest_games_table = GamesTable(latest_games)
    latest_tournaments_table = TournamentsTable(latest_tournaments)
    top_10_dan_table = Top10DanTable(top_10_dan)
    top_10_kyu_table = Top10KyuTable(top_10_kyu)

    return render(
        request,
        "beta.index.html",
        {
            "latest_games_table": latest_games_table,
            "latest_tournaments_table": latest_tournaments_table,
            "top_10_dan_table": top_10_dan_table,
            "top_10_kyu_table": top_10_kyu_table,
        },
    )
