# Python Imports
import datetime

# AGAGD Imports
import agagd_core.models as agagd_models

# Django Tables Imports
from agagd_core.tables.games import GamesTable
from agagd_core.tables.players import PlayersTournamentTable
from agagd_core.tables.top_players import TopDanTable, TopKyuTable
from agagd_core.tables.tournaments import TournamentsTable
from django.shortcuts import render
from django.template.response import TemplateResponse

# Django Imports
from django.views.generic.detail import DetailView


class FrontPageView(DetailView):
    template_name = "frontpage.html"

    def __get_latest_games(self):
        latest_games = agagd_models.Game.objects.values(
            "game_date",
            "handicap",
            "pin_player_1",
            "pin_player_2",
            "tournament_code",
            "result",
        ).order_by("-game_date")[:20]

        return latest_games

    def __get_latest_tournaments(self):
        latest_tournaments = agagd_models.Tournament.objects.values(
            "description",
            "tournament_code",
            "total_players",
            "tournament_date",
            "elab_date",
        ).order_by("-elab_date")[:20]

        return latest_tournaments

    def __get_top_dan_kyu(self):
        return agagd_models.Players.objects.all()

    def __get_top_dan(self):
        top_dan = (
            self.__get_top_dan_kyu()
            .filter(rating__gt=0)
            .filter(
                elab_date__gte=datetime.datetime.now() - datetime.timedelta(weeks=52)
            )
            .order_by("-rating")[:5]
        )

        return top_dan

    def __get_top_kyu(self):
        top_kyu = (
            self.__get_top_dan_kyu()
            .filter(rating__lt=0)
            .filter(
                elab_date__gte=datetime.datetime.now() - datetime.timedelta(weeks=52)
            )
            .order_by("-rating")[:5]
        )

        return top_kyu

    def get(self, request):
        # Index Tables
        latest_games_table = GamesTable(self.__get_latest_games())
        latest_tournaments_table = TournamentsTable(self.__get_latest_tournaments())
        top_dan_table = TopDanTable(self.__get_top_dan())
        top_kyu_table = TopKyuTable(self.__get_top_kyu())

        context = locals()
        context["latest_games_table"] = latest_games_table
        context["latest_tournaments_table"] = latest_tournaments_table
        context["top_dan_table"] = top_dan_table
        context["top_kyu_table"] = top_kyu_table

        return TemplateResponse(request, self.template_name, context)
