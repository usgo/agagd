import agagd_core.models as agagd_models
from agagd_core.tables.all_players import AllPlayersTable
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig


class AllPlayersPageView(DetailView):
    template_name = "all_players_page.html"

    def get(self, request):
        all_players = (
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

        all_players_table = AllPlayersTable(all_players)

        RequestConfig(request, paginate={"per_page": 50}).configure(all_players_table)

        context = locals()
        context["all_players_table"] = all_players_table
        context["page_title"] = "Ratings"

        return TemplateResponse(request, self.template_name, context)
