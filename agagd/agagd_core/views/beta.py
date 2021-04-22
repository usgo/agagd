# Datetime Imports
from datetime import date, datetime, timedelta

# AGAGD Models Import
import agagd_core.models as agagd_models

# AGAGD Tables Import
import agagd_core.tables.beta as agagd_tables

# Django Imports
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

# Django Table Imports
from django_tables2 import RequestConfig


def agagd_paginator_helper(
    request, query_list_object, max_rows_per_page=50, page_request_get_value="pg"
):
    paginator = Paginator(query_list_object, max_rows_per_page)

    page_number = request.GET.get(page_request_get_value, 1)

    try:
        query_list_object_with_page_information = paginator.page(page_number)
    except PageNotAnInteger:
        query_list_object_with_page_information = paginator.page(1)
    except EmptyPage:
        query_list_object_with_page_information = paginator.page(paginator.num_pages)

    return query_list_object_with_page_information


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
        agagd_models.Member.objects.select_related("chapter_id")
        .filter(status="accepted")
        .filter(players__rating__isnull=False)
        .exclude(type__iexact="e-journal")
        .exclude(type__iexact="chapter")
        .exclude(type__iexact="library")
        .exclude(type__iexact="institution")
        .values(
            "chapter_id",
            "member_id",
            "chapter_id__name",
            "full_name",
            "type",
            "players__rating",
            "state",
            "players__sigma",
        )
        .order_by("-players__rating")
    )

    mobile_column_attrs = "d-none d-lg-table-cell d-xl-table-cell"

    list_all_players_columns = (
        {"name": "Name", "attrs": None},
        {"name": "Chapter", "attrs": None},
        {"name": "State", "attrs": mobile_column_attrs},
        {"name": "Type", "attrs": mobile_column_attrs},
        {"name": "Rating", "attrs": None},
        {"name": "Sigma", "attrs": mobile_column_attrs},
    )

    list_all_players_with_pagination = agagd_paginator_helper(
        request, list_all_players_query
    )

    return render(
        request,
        "agagd_core/players_list.html",
        {
            "mobile_column_attrs": mobile_column_attrs,
            "list_all_players_columns": list_all_players_columns,
            "list_all_players_data": list_all_players_with_pagination,
            "page_title": "Members Ratings",
        },
    )
