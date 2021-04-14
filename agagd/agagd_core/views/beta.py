# Datetime Imports
from datetime import datetime, timedelta, date

# AGAGD Models Import
import agagd_core.models as agagd_models

# AGAGD Tables Import
import agagd_core.tables.beta as agagd_tables

# Django Imports
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Q

# Django Table Imports
from django_tables2 import RequestConfig


def index(request):
    game_list = agagd_models.Game.objects.filter(
        game_date__gte=datetime.now() - timedelta(days=180)
    ).order_by("-game_date")
    table = agagd_tables.GameTable(game_list, prefix="games")
    topDanList = agagd_models.TopDan.objects.values()
    topDanTable = agagd_tables.TopDanTable(topDanList)
    topKyuList = agagd_models.TopKyu.objects.values()
    topKyuTable = agagd_tables.TopKyuTable(topKyuList)
    mostRatedGamesPastYearList = agagd_models.MostRatedGamesPastYear.objects.values()
    mostRatedGamesTable = agagd_tables.MostRatedGamesPastYearTable(
        mostRatedGamesPastYearList
    )
    mostTournamentsPastYearList = agagd_models.MostTournamentsPastYear.objects.values()
    mostTournamentsPastYearTable = agagd_tables.MostTournamentsPastYearTable(
        mostTournamentsPastYearList
    )
    RequestConfig(request).configure(table)
    tourneys = agagd_models.Tournament.objects.all().order_by("-tournament_date")
    t_table = agagd_tables.TournamentTable(tourneys, prefix="tourneys")
    RequestConfig(request, paginate={"per_page": 10}).configure(t_table)

    return render(
        request,
        "agagd_core/index.beta.html",
        {
            "table": table,
            "top_dan_table": topDanTable,
            "top_kyu_table": topKyuTable,
            "most_rated_games_table": mostRatedGamesTable,
            "most_tournaments_table": mostTournamentsPastYearTable,
            "tournaments": t_table,
        },
    )


def list_all_players(request):
    list_all_players_query = (
        agagd_models.Member.objects.filter(
            Q(chapter_id=F("chapters__member_id")) | Q(chapters__member_id__isnull=True)
        )
        .filter(Q(member_id=F("players__pin_player")))
        .filter(status="accepted")
        .exclude(players__rating__isnull=True)
        .exclude(type="chapter")
        .exclude(type="e-journal")
        .exclude(type="library")
        .exclude(type="institution")
        .values(
            "full_name",
            "member_id",
            "type",
            "players__rating",
            "chapter_id",
            "state",
            "players__sigma",
        )
        .order_by("-players__rating")
    )

    list_all_players_table = agagd_tables.ListAllPlayersTable(list_all_players_query)
    RequestConfig(request, paginate={"per_page": 50}).configure(list_all_players_table)

    return render(
        request,
        "agagd_core/players_list.html",
        {"list_all_players_table": list_all_players_table},
    )
