import agagd_core.models as agagd_models
from agagd_core.helpers.pagination import agagd_paginator_helper
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView


class AllTournamentsPageView(DetailView):
    template_name = "beta.tournaments_list.html"

    def get(self, request):
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

        context = locals()
        context["mobile_columns"] = mobile_columns
        context["table_headers"] = table_headers
        context["list_all_tournaments"] = list_all_tournaments_with_pagination
        context["page_title"] = "Tournaments"

        return TemplateResponse(request, "beta.tournaments_list.html", context)
