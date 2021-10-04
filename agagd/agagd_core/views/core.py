import logging
from datetime import date, datetime, timedelta

from agagd_core.json_response import JsonResponse
from agagd_core.models import (
    Chapters,
    Country,
    Game,
    Member,
    MostRatedGamesPastYear,
    MostTournamentsPastYear,
    TopDan,
    TopKyu,
    Tournament,
)
from agagd_core.tables.core import (
    AllPlayerRatingsTable,
    GameTable,
    MemberTable,
    MostRatedGamesPastYearTable,
    MostTournamentsPastYearTable,
    OpponentTable,
    SecondaryGameTable,
    TopDanTable,
    TopKyuTable,
    TournamentPlayedTable,
    TournamentTable,
)
from django.core import exceptions
from django.core.paginator import PageNotAnInteger
from django.db.models import Count, F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView
from django_tables2 import RequestConfig

logger = logging.getLogger("agagd.core.views")


@require_POST
def find_member_vs(request, member_id):
    opponent = get_object_or_404(Member, member_id=request.POST.get("opponent_id", ""))
    return HttpResponseRedirect(
        reverse("member_vs", args=(member_id, opponent.member_id))
    )


def member_vs(request, member_id, other_id):
    player_1 = get_object_or_404(Member, member_id=member_id)
    player_2 = get_object_or_404(Member, member_id=other_id)
    game_list = Game.objects.filter(
        Q(pin_player_1=player_1, pin_player_2=player_2)
        | Q(pin_player_1=player_2, pin_player_2=player_1)
    ).order_by("-game_date")
    table = GameTable(game_list)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(
        request,
        "agagd_core/member_vs.html",
        {"table": table, "player_1": player_1, "player_2": player_2},
    )


def chapter_code_redirect(request, chapter_code):
    # Try the lookup with the 4-letter chapter code. These are deprecated,
    # but we continue to support them in case users have chapter pages bookmarked.
    chapter = get_object_or_404(Chapters, code=chapter_code)
    return redirect("chapter_detail", chapter_id=chapter.pk, permanent=True)


def country_detail(request, country_name):
    member_table = MemberTable(
        Member.objects.filter(country=country_name)
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

    RequestConfig(request, paginate={"per_page": 100}).configure(member_table)

    return render(
        request,
        "agagd_core/country.html",
        {"country_name": country_name, "member_table": member_table},
    )
