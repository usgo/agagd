import agagd_core.models as agagd_models
from agagd_core.helpers.pagination import agagd_paginator_helper
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView


class TournamentDetailPageView(DetailView):
    template_name = "beta.tournament_detail.html"

    def get(self, request, *args, **kwargs):
        code = self.kwargs.get("code")
        try:
            tournament = agagd_models.Tournament.objects.get(pk=code)
        except agagd_models.Tournament.DoesNotExist:
            raise Http404(f"Tournament {code} does not exist.")

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

        context = locals()
        context["page_title"] = tournament_information["tournament_code"]
        context["tournament_information"] = tournament_information
        context["tournament_games"] = tournament_games
        context["tournament_table_headers"] = tournament_table_headers
        context["tournament_game_table_headers"] = tournament_game_table_headers

        return TemplateResponse(request, self.template_name, context)
