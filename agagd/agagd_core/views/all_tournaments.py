import agagd_core.models as agagd_models
from agagd_core.tables.all_tournaments import AllTournamentsTable
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig


class AllTournamentsPageView(DetailView):
    template_name = "all_tournaments_page.html"

    def get(self, request):
        all_tournaments = agagd_models.Tournament.objects.values(
            "tournament_code",
            "description",
            "tournament_date",
            "elab_date",
            "city",
            "state",
            "rounds",
            "total_players",
        ).order_by("-tournament_date")

        all_tournaments_table = AllTournamentsTable(all_tournaments)
        RequestConfig(request, paginate={"per_page": 50}).configure(
            all_tournaments_table
        )

        context = locals()
        context["all_tournaments_table"] = all_tournaments_table
        context["page_title"] = "Tournaments"

        return TemplateResponse(request, self.template_name, context)
