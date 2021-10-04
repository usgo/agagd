from agagd_core.models import Member
from agagd_core.tables.search import SearchResultsTable
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView
from django_tables2 import RequestConfig


class SearchView(DetailView):
    template_name = "search_page.html"
    search_results_template_name = "search_results.html"

    def get(self, request):
        query = request.GET.get("q", "")

        if not query:
            return TemplateResponse(request, self.template_name)

        if query.isdigit():
            member_id = [int(query)]
            return HttpResponseRedirect(reverse("member_detail", args=member_id))

        member_table_data = (
            Member.objects.filter(Q(member_id=F("players__pin_player")))
            .filter(full_name__icontains=query)
            .values(
                "member_id",
                "chapter_id",
                "renewal_due",
                "state",
                "players__rating",
                "country",
                "full_name",
                "family_name",
            )
            .order_by("family_name")
        )

        self.template_name = self.search_results_template_name

        member_results_table = SearchResultsTable(member_table_data)
        RequestConfig(request, paginate={"per_page": 25}).configure(
            member_results_table
        )

        context = locals()
        context["search_query"] = query
        context["member_results_table"] = member_results_table

        return TemplateResponse(request, self.template_name, context)
