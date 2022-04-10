import agagd_core.models as agagd_models
from agagd_core.tables.tournaments import (
    TournamentsGamesTable,
    TournamentsInformationTable,
)
from django.db.models import CharField
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig


class TournamentDetailPageView(DetailView):
    template_name = "tournament_detail.html"

    def get(self, request, *args, **kwargs):
        code = self.kwargs.get("code")
        try:
            tournament = agagd_models.Tournament.objects.get(pk=code)
        except agagd_models.Tournament.DoesNotExist:
            raise Http404(f"Tournament {code} does not exist.")

        tournament_information_table = TournamentsInformationTable(
            [tournament.__dict__]
        )

        tournament_games = tournament.games_in_tourney.values(
            "game_date",
            "pin_player_1",
            "pin_player_2",
            "handicap",
            "komi",
            "result",
            full_name_and_id_1=Concat(
                "pin_player_1__full_name",
                V(" ("),
                "pin_player_1",
                V(")"),
                output_field=CharField(),
            ),
            full_name_and_id_2=Concat(
                "pin_player_2__full_name",
                V(" ("),
                "pin_player_2",
                V(")"),
                output_field=CharField(),
            ),
        )

        tournament_games_table = TournamentsGamesTable(tournament_games)

        RequestConfig(request, paginate={"per_page": 50}).configure(
            tournament_games_table
        )

        context = locals()
        context["page_title"] = tournament.pk
        context["tournament_information_table"] = tournament_information_table
        context["tournament_games_table"] = tournament_games_table

        return TemplateResponse(request, self.template_name, context)
