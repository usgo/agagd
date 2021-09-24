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
