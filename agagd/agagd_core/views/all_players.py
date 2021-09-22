import agagd_core.models as agagd_models
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView


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


class AllPlayersPageView(DetailView):
    template_name = "beta.players_list.html"

    def get(self, request):
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

        context = locals()
        context["mobile_column_attrs"] = mobile_column_attrs
        context["list_all_players_columns"] = list_all_players_columns
        context["list_all_players_data"] = list_all_players_with_pagination
        context["page_title"] = "members ratings"

        return TemplateResponse(request, self.template_name, context)
