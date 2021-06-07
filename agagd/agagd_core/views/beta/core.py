# Datetime Imports
from datetime import date, datetime, timedelta

# AGAGD Models Import
import agagd_core.models as agagd_models
from agagd_core.tables.beta import (
    GamesTable,
    PlayersTournamentTable,
    Top10DanTable,
    Top10KyuTable,
    TournamentsTable,
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

# Django Imports
from django.views.generic import ListView

# Django Table Imports
from django_tables2 import LazyPaginator, RequestConfig


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


def get_opponent_from_game_helper(player_id, game=None):
    if game.pin_player_1 == player_id:
        return game.pin_player_1
    return game.pin_player_2


def get_game_date_from_game_helper(game):
    if game.game_date == "0000-00-00":
        return None
    return game.game_date


def winner_of_game_helper(game):
    if game.result == game.color_1:
        return game.pin_player_1
    elif game.result == game.color_2:
        return game.pin_player_2
    return None


def loser_of_game_helper(game):
    if game.result == game.color_1:
        return game.pin_player_2
    elif game.result == game.color_2:
        return game.pin_player_1
    return None


def tournament_list_helper(player_id, game_list):
    """ Creates a list with the tournament data from the player's games. """
    tournaments_data = {}

    for game in game_list:
        temp_tournament_data = tournaments_data.get(game.tournament_code.pk, {})
        temp_tournament_data["tournament"] = game.tournament_code
        temp_tournament_data["won"] = temp_tournament_data.get("won", 0)
        temp_tournament_data["lost"] = temp_tournament_data.get("lost", 0)

        game_date = get_game_date_from_game_helper(game)

        temp_tournament_data["date"] = temp_tournament_data.get("date", game_date)

        if winner_of_game_helper(game) == player_id:
            temp_tournament_data["won"] += 1
        elif loser_of_game_helper(game) == player_id:
            temp_tournament_data["lost"] += 1

        tournaments_data[game.tournament_code.pk] = temp_tournament_data

    return tournaments_data


def opponents_list_hepler(player_id, games_list):
    """ Creates a list with the opponent data from the player's games. """
    opponent_data = {}

    for game in games_list:
        game_date = get_game_date_from_game_helper(game)

        opponent_id = get_opponent_from_game_helper(player_id, game)
        temp_opponent_data = opponent_data.get(opponent_data, {})
        temp_opponent_data["opponent"] = opponent_id
        temp_opponent_data["total"] = opponent_data.get("total", 0)
        temp_opponent_data["won"] = opponent_data.get("won", 0)
        temp_opponent_data["lost"] = opponent_data.get("lost", 0)

        if winner_of_game_helper(game) == player_id:
            temp_opponent_data["won"] += 1
        elif loser_of_game_helper(game) == player_id:
            temp_opponent_data["lost"] += 1

        opponent_data[opponent_id] = temp_opponent_data


def player_profile(request, player_id):
    player = agagd_models.Member.objects.get(member_id=player_id)

    player_games = agagd_models.Game.objects.filter(
        Q(pin_player_1__exact=player_id) | Q(pin_player_2__exact=player_id)
    ).order_by("-game_date")

    player_rating = agagd_models.Players.objects.filter(
        Q(pin_player__exact=player_id)
    ).values("pin_player", "rating", "sigma")

    # tournaments_data = tournament_list_helper(player_id, player_games)
    # tournaments_table = PlayersTournamentTable(tournaments_data.values(), player)

    # opponents_data = opponents_list_hepler(player_id, player_games)
    # opponents_table = PlayersOpponentTable(opponents_data.values(), player)

    return render(
        request,
        "beta.player_profile.html",
        {
            "player": player,
            # "tournaments_table": tournaments_table,
            # "opponents_table": opponents_table,
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
