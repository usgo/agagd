# Datetime Imports
from datetime import date, datetime, timedelta

# AGAGD Models Import
import agagd_core.models as agagd_models

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
    latest_games_table_headers = {
        "game_date": "Date",
        "tournament_code_id": "Tournament Code",
        "pin_player_1": "White",
        "pin_player_2": "Black",
        "handicap": "Handicap",
        "komi": "Komi",
    }

    latest_games = agagd_models.Game.objects.values(
        "game_date",
        "tournament_code_id",
        "pin_player_1",
        "pin_player_2",
        "handicap",
        "komi",
    ).order_by("-game_date")[:25]

    latest_tournaments_table_headers = {
        "tournament_date": "Date",
        "elab_date": "Rated",
        "tournament_code": "Tournament Code",
        "city": "City",
        "state": "State",
        "rounds": "Rounds",
    }

    latest_tournaments = agagd_models.Tournament.objects.values(
        "tournament_date", "elab_date", "tournament_code", "city", "state", "rounds"
    ).order_by("-elab_date")[:25]

    top_10_kyu_dan_table_headers = {
        "pin_player": "Player",
        "rating": "Rating",
        "sigma": "Sigma",
    }

    top_10_dan = (
        agagd_models.Players.objects.filter(rating__gt=0)
        .values("pin_player", "rating", "sigma")
        .order_by("-rating")[0:10]
    )

    top_10_kyu = (
        agagd_models.Players.objects.filter(rating__lt=0)
        .values("pin_player", "rating", "sigma")
        .order_by("-rating")[0:10]
    )

    return render(
        request,
        "beta.index.html",
        {
            "latest_games": latest_games,
            "latest_tournaments": latest_tournaments,
            "top_10_dan": top_10_dan,
            "top_10_kyu": top_10_kyu,
            "latest_games_table_headers": latest_games_table_headers,
            "latest_tournaments_table_headers": latest_tournaments_table_headers,
            "top_10_kyu_dan_table_headers": top_10_kyu_dan_table_headers,
        },
    )


def tournament_detail(request, code):
    try:
        tournament = agagd_models.Tournament.objects.get(pk=code)
    except Tournament.DoesNotExist:
        raise Http404(f"Tournament {name} does not exist.")

    tournament_information = {
        "tournament_code": tournament.pk,
        "description": tournament.description,
        "elab_date": tournament.elab_date,
        "tournament_date": tournament.tournament_date,
        "state": tournament.state,
    }

    tournament_table_headers = {
        "tournament_code": "Code",
        "description": "Description",
        "tournament_date": "Date",
        "elab_date": "Rated",
        "city": "City",
        "state": "State",
        "rounds": "Rounds",
        "total_players": "No. Players",
    }

    tournament_games = agagd_paginator_helper(
        request,
        tournament.games_in_tourney.values(
            "game_date", "pin_player_1", "pin_player_2", "handicap", "komi"
        ),
    )

    tournament_game_table_headers = {
        "game_date": "Date",
        "pin_player_1": "White",
        "pin_player_2": "Black",
        "handicap": "Handicap",
        "komi": "Komi",
    }

    return render(
        request,
        "beta.tournament_detail.html",
        {
            "page_title": tournament_information["tournament_code"],
            "tournament_information": tournament_information,
            "tournament_games": tournament_games,
            "tournament_table_headers": tournament_table_headers,
            "tournament_game_table_headers": tournament_game_table_headers,
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
        "beta.players_list.html",
        {
            "mobile_column_attrs": mobile_column_attrs,
            "list_all_players_columns": list_all_players_columns,
            "list_all_players_data": list_all_players_with_pagination,
            "page_title": "Members Ratings",
        },
    )


def list_all_tournaments(request):
    mobile_column_default_attrs = "d-none d-lg-table-cell d-xl-table-cell"

    mobile_columns = {
        "city": mobile_column_default_attrs,
        "state": mobile_column_default_attrs,
        "total_players": mobile_column_default_attrs,
    }

    table_headers = {
        "tournament_code": "Code",
        "description": "Description",
        "tournament_date": "Date",
        "elab_date": "Rated",
        "city": "City",
        "state": "State",
        "rounds": "Rounds",
        "total_players": "No. Players",
    }

    list_all_tournaments_query = agagd_models.Tournament.objects.values(
        "tournament_code",
        "description",
        "tournament_date",
        "elab_date",
        "city",
        "state",
        "rounds",
        "total_players",
    ).order_by("-tournament_date")

    list_all_tournaments_with_pagination = agagd_paginator_helper(
        request, list_all_tournaments_query
    )

    return render(
        request,
        "beta.tournaments_list.html",
        {
            "mobile_columns": mobile_columns,
            "table_headers": table_headers,
            "list_all_tournaments": list_all_tournaments_with_pagination,
            "page_title": "Tournaments",
        },
    )
