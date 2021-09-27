# Python Imports
import datetime

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
from django.shortcuts import render
from django.template.response import TemplateResponse

# Django Imports
from django.views.generic.detail import DetailView


class FrontPageView(DetailView):
    template_name = "beta.index.html"

    def _get_latest_games(self):
        latest_games = agagd_models.Game.objects.values(
            "game_date",
            "handicap",
            "pin_player_1",
            "pin_player_2",
            "tournament_code",
            "result",
        ).order_by("-game_date")[:20]

        return latest_games

    def get(self, request):
        latest_tournaments = agagd_models.Tournament.objects.all().order_by(
            "-elab_date"
        )[:20]

        top_10_dan_kyu = agagd_models.Players.objects.all()

        top_10_dan = (
            top_10_dan_kyu.filter(rating__gt=0)
            .filter(
                elab_date__gte=datetime.datetime.now() - datetime.timedelta(weeks=52)
            )
            .order_by("-rating")[:10]
        )
        top_10_kyu = (
            top_10_dan_kyu.filter(rating__lt=0)
            .filter(
                elab_date__gte=datetime.datetime.now() - datetime.timedelta(weeks=52)
            )
            .order_by("-rating")[:10]
        )

        # Index Tables
        latest_games_table = GamesTable(self._get_latest_games())
        latest_tournaments_table = TournamentsTable(latest_tournaments)
        top_10_dan_table = Top10DanTable(top_10_dan)
        top_10_kyu_table = Top10KyuTable(top_10_kyu)

        context = locals()
        context["latest_games_table"] = latest_games_table
        context["latest_tournaments_table"] = latest_tournaments_table
        context["top_10_dan_table"] = top_10_dan_table
        context["top_10_kyu_table"] = top_10_kyu_table

        return TemplateResponse(request, self.template_name, context)
