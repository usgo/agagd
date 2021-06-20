# Date Imports
from datetime import date

# AGAGD Models Imports
import agagd_core.models as agagd_models

# AGAGD Django Tables Imports
from agagd_core.tables.beta import (
    GamesTable,
    PlayersInformationTable,
    PlayersOpponentTable,
    PlayersTournamentTable,
)

# Django Imports
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render

# Django Tables 2 Imports
from django_tables2 import RequestConfig


def players_profile(request, player_id):
    player = agagd_models.Member.objects.get(member_id=player_id)

    player_games = agagd_models.Game.objects.filter(
        Q(pin_player_1__exact=player_id) | Q(pin_player_2__exact=player_id)
    ).order_by("-game_date")

    player_rating = agagd_models.Players.objects.filter(
        Q(pin_player__exact=player_id)
    ).values("pin_player", "rating", "sigma")

    # compute additional tables for opponents & tournament info. here
    # TODO: refactor this into something nicer.
    opponent_data = {}
    tourney_data = {}
    for game in player_games:
        try:
            t_dat = tourney_data.get(game.tournament_code.pk, {})
            t_dat["tournament"] = game.tournament_code
            t_dat["won"] = t_dat.get("won", 0)
            t_dat["lost"] = t_dat.get("lost", 0)

            # Set default game_date to None
            game_date = None

            # Check for 0000-00-00 dates
            if game.game_date != u"0000-00-00":
                game_date = game.game_date

            t_dat["date"] = t_dat.get("date", game_date)

            op = game.player_other_than(player)
            opp_dat = opponent_data.get(op, {})
            opp_dat["opponent"] = op
            opp_dat["total"] = opp_dat.get("total", 0) + 1
            opp_dat["won"] = opp_dat.get("won", 0)
            opp_dat["lost"] = opp_dat.get("lost", 0)
            if game.won_by(player):
                opp_dat["won"] += 1
                t_dat["won"] += 1
            else:
                opp_dat["lost"] += 1
                t_dat["lost"] += 1
            opponent_data[op] = opp_dat
            tourney_data[game.tournament_code.pk] = t_dat
        except ObjectDoesNotExist:
            print("failing game_id: %s" % game.pk)

    opp_table = PlayersOpponentTable(opponent_data.values())
    RequestConfig(request, paginate={"per_page": 10}).configure(opp_table)

    t_table = PlayersTournamentTable(
        tourney_data.values(),
        sorted(
            tourney_data.values(),
            key=lambda d: d.get("date", date.today()) or date.today(),
            reverse=True,
        ),
        prefix="ts_played",
    )
    RequestConfig(request, paginate={"per_page": 10}).configure(t_table)

    player_games_table = GamesTable(
        player_games.values(
            "game_date",
            "handicap",
            "pin_player_1",
            "pin_player_2",
            "tournament_code",
            "result",
        )
    )

    player_information_dict = player.__dict__
    player_information_dict["rating"] = player_rating[0]["rating"]

    players_information_table = PlayersInformationTable([player_information_dict])

    return render(
        request,
        "beta.player_profile.html",
        {
            "page_title": "Player Profile | {}".format(player.full_name),
            "player": player,
            "player_rating": player_rating[0],
            "player_games_table": player_games_table,
            "players_information_table": players_information_table,
            "player_opponents_table": opp_table,
            "player_tournaments_table": t_table,
        },
    )
