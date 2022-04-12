# AGAGD Models Imports
import agagd_core.models as agagd_models
from agagd_core.tables.games import GamesTable

# AGAGD Django Tables Imports
from agagd_core.tables.players import (
    PlayersInformationTable,
    PlayersOpponentTable,
    PlayersTournamentTable,
)

# Django Imports
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, CharField, Count, F, IntegerField, Q, When
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView

# Django Tables 2 Imports
from django_tables2 import RequestConfig


class PlayersProfilePageView(DetailView):
    template_name = "players_profile_page.html"

    def get(self, request, *args, **kwargs):
        player_id = self.kwargs.get("player_id")
        try:
            player = (
                agagd_models.Member.objects.exclude(status="pending")
                .exclude(type="chapter")
                .get(member_id=player_id)
            )
        except ObjectDoesNotExist:
            raise Http404("Player Profile Not Found.")

        player_games = agagd_models.Game.objects.filter(
            Q(pin_player_1__exact=player_id) | Q(pin_player_2__exact=player_id)
        ).order_by("-game_date")

        player_rating = agagd_models.Players.objects.filter(
            Q(pin_player__exact=player_id)
        ).values("pin_player", "rating", "sigma")

        # Q objects to select games played by the player ...
        Q_played = Q(pin_player_1__exact=player_id) | Q(pin_player_2__exact=player_id)
        # ... won by the player ...
        Q_won = Q(pin_player_1__exact=player_id, result__exact="W") | Q(
            pin_player_2__exact=player_id, result__exact="B"
        )
        # ... and lost by the player
        Q_lost = Q(pin_player_1__exact=player_id, result__exact="B") | Q(
            pin_player_2__exact=player_id, result__exact="W"
        )

        opponents_queryset = (
            agagd_models.Game.objects.filter(Q_played)
            .annotate(
                opponent_id=Case(
                    When(
                        pin_player_1__exact=player_id,
                        then=F("pin_player_2"),
                    ),
                    When(
                        pin_player_2__exact=player_id,
                        then=F("pin_player_1"),
                    ),
                    output_field=IntegerField(),
                ),
                opponent_full_name=Case(
                    When(
                        pin_player_1__exact=player_id,
                        then=F("pin_player_2__full_name"),
                    ),
                    When(
                        pin_player_2__exact=player_id,
                        then=F("pin_player_1__full_name"),
                    ),
                    output_field=CharField(),
                ),
            )
            .values("opponent_id", "opponent_full_name")
            .annotate(
                won=Count("game_id", filter=Q_won),
                lost=Count("game_id", filter=Q_lost),
                total=F("won") + F("lost"),
            )
            .order_by("-total", "-won")
        )
        opponents_table = PlayersOpponentTable(opponents_queryset)
        RequestConfig(request, paginate={"per_page": 10}).configure(opponents_table)

        tournaments_queryset = (
            agagd_models.Game.objects.filter(Q_played)
            .values("tournament_code")
            .annotate(
                tournament_date=F("tournament_code__tournament_date"),
                tournament_total_players=F("tournament_code__total_players"),
                date=F("game_date"),
                won=Count("game_id", filter=Q_won),
                lost=Count("game_id", filter=Q_lost),
            )
            .order_by("-date")
        )
        tournaments_table = PlayersTournamentTable(tournaments_queryset)
        RequestConfig(request, paginate={"per_page": 10}).configure(tournaments_table)

        player_games_table = GamesTable(
            player_games.values(
                "handicap",
                "result",
                date=F("game_date"),
                tournament=F("tournament_code"),
                white=F("pin_player_1"),
                black=F("pin_player_2"),
                white_name=F("pin_player_1__full_name"),
                black_name=F("pin_player_2__full_name"),
            )
        )

        player_information_dict = player.__dict__
        player_information_dict["rating"] = player_rating[0]["rating"]

        try:
            chapter_name = agagd_models.Chapters.objects.get(
                member_id=player.chapter_id_id
            ).name
            player_information_dict["members_chapter_name"] = chapter_name
        except:
            player_information_dict["members_chapter_name"] = None

        players_information_table = PlayersInformationTable([player_information_dict])

        context = locals()
        context["page_title"] = "Player Profile | {}".format(player.full_name)
        context["player"] = player
        context["player_rating"] = player_rating[0]
        context["player_games_table"] = player_games_table
        context["players_information_table"] = players_information_table
        context["player_opponents_table"] = opponents_table
        context["player_tournaments_table"] = tournaments_table

        return TemplateResponse(request, self.template_name, context)
