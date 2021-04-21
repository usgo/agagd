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
    ChapterMemberTable,
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


def index(request):
    game_list = Game.objects.filter(
        game_date__gte=datetime.now() - timedelta(days=180)
    ).order_by("-game_date")
    table = GameTable(game_list, prefix="games")
    topDanList = TopDan.objects.values()
    topDanTable = TopDanTable(topDanList)
    topKyuList = TopKyu.objects.values()
    topKyuTable = TopKyuTable(topKyuList)
    mostRatedGamesPastYearList = MostRatedGamesPastYear.objects.values()
    mostRatedGamesTable = MostRatedGamesPastYearTable(mostRatedGamesPastYearList)
    mostTournamentsPastYearList = MostTournamentsPastYear.objects.values()
    mostTournamentsPastYearTable = MostTournamentsPastYearTable(
        mostTournamentsPastYearList
    )
    RequestConfig(request).configure(table)
    tourneys = Tournament.objects.all().order_by("-tournament_date")
    t_table = TournamentTable(tourneys, prefix="tourneys")
    RequestConfig(request, paginate={"per_page": 10}).configure(t_table)

    return render(
        request,
        "agagd_core/index.html",
        {
            "table": table,
            "top_dan_table": topDanTable,
            "top_kyu_table": topKyuTable,
            "most_rated_games_table": mostRatedGamesTable,
            "most_tournaments_table": mostTournamentsPastYearTable,
            "tournaments": t_table,
        },
    )


@require_GET
def search(request):
    query = request.GET.get("q", "")

    if not query:
        return HttpResponseRedirect("/")

    try:
        member_id = int(query)
        return HttpResponseRedirect(reverse("member_detail", args=(member_id,)))
    except ValueError:
        members_query = (
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

        member_table = MemberTable(members_query)

        try:
            RequestConfig(request, paginate={"per_page": 100}).configure(member_table)
        except PageNotAnInteger:
            RequestConfig(request, paginate=False).configure(member_table)

        return render(
            request,
            "agagd_core/search_player.html",
            {"member_table": member_table, "query": query},
        )


def member_ratings(request, member_id):
    # returns a members rating data as a json dict for graphing
    try:
        player = Member.objects.get(pk=member_id)
        ratings = player.ratings_set.all().order_by("elab_date")
        ratings_dict = [
            {"sigma": r.sigma, "elab_date": r.elab_date, "rating": r.rating}
            for r in ratings
            if r.elab_date != None
        ]
        if len(ratings_dict) <= 1:
            logger.debug("Ratings error: only one rating")
            return JsonResponse(
                {"result": "error", "message": "Only one rated game. Not enough data"}
            )
        return JsonResponse(ratings_dict)
    except:
        logger.debug("Ratings error", exc_info=1)
        return JsonResponse({"result": "error"})


def member_detail(request, member_id):
    """
    The member detail page.
    Fetches the most recent games played and puts them in a Games Table.
    Fetches the list of ratings and puts them in a format for graphing.
    Computes the tournament data and opponent data for respective tables.
    """
    game_list = Game.objects.filter(
        Q(pin_player_1__exact=member_id) | Q(pin_player_2__exact=member_id)
    ).order_by("-game_date", "round")
    table = GameTable(game_list, prefix="games")
    RequestConfig(request, paginate={"per_page": 20}).configure(table)

    player = Member.objects.get(member_id=member_id)

    try:
        chapter = Chapters.objects.get(member_id=player.chapter_id.member_id)
    except exceptions.ObjectDoesNotExist:
        chapter = None

    ratings = player.ratings_set.all().order_by("-elab_date")
    if len(ratings) > 0:
        max_rating = max([r.rating for r in ratings])
        last_rating = ratings[0]
    else:
        max_rating = last_rating = None

    # compute additional tables for opponents & tournament info. here
    # TODO: refactor this into something nicer.
    opponent_data = {}
    tourney_data = {}
    for game in game_list:
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
        except exceptions.ObjectDoesNotExist:
            print("failing game_id: %s" % game.pk)

    opp_table = OpponentTable(opponent_data.values(), player, prefix="opp")
    opp_table.this_player = player
    RequestConfig(request, paginate={"per_page": 10}).configure(opp_table)

    t_table = TournamentPlayedTable(
        sorted(
            tourney_data.values(),
            key=lambda d: d.get("date", date.today()) or date.today(),
            reverse=True,
        ),
        prefix="ts_played",
    )
    RequestConfig(request, paginate={"per_page": 10}).configure(t_table)

    return render(
        request,
        "agagd_core/member.html",
        {
            "table": table,
            "player": player,
            "chapter": chapter,
            "rating": last_rating,
            "max_rating": max_rating,
            "num_games": len(game_list),
            "opponents": opp_table,
            "tourneys": t_table,
        },
    )


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


def tournament_detail(request, tourn_code):
    tourney = Tournament.objects.get(pk=tourn_code)
    secondary_gametable = SecondaryGameTable(tourney.games_in_tourney.all())
    RequestConfig(request, paginate={"per_page": 20}).configure(secondary_gametable)
    return render(
        request,
        "agagd_core/tourney.html",
        {"secondary_gametable": secondary_gametable, "tournament": tourney},
    )


def chapter_detail(request, chapter_id):
    chapter = get_object_or_404(Chapters, member_id=chapter_id)
    chapter_member_table = ChapterMemberTable(
        Member.objects.filter(chapter_id=chapter_id)
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
    return render(
        request,
        "agagd_core/chapter.html",
        {"member_table": chapter_member_table, "chapter": chapter},
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


def all_player_ratings(request):
    all_player_ratings_query = (
        Member.objects.select_related("chapter_id")
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

    all_player_ratings_table = AllPlayerRatingsTable(all_player_ratings_query)
    RequestConfig(request, paginate={"per_page": 50}).configure(
        all_player_ratings_table
    )

    return render(
        request,
        "agagd_core/all_player_ratings.html",
        {"all_player_ratings_table": all_player_ratings_table},
    )


@require_GET
def tournament_list(request):
    tourneys = Tournament.objects.order_by("-tournament_date")
    details = request.GET.get("details", "")
    from_date = request.GET.get("from_date", "")
    to_date = request.GET.get("to_date", "")

    if details:
        for search_token in details.split():
            query = search_token.lower()
            tourneys = tourneys.filter(
                Q(description__icontains=query)
                | Q(city__icontains=query)
                | Q(state__icontains=query)
            )

    if from_date:
        tourneys = tourneys.filter(
            tournament_date__gte=datetime.strptime(from_date, "%m/%d/%Y")
        )

    if to_date:
        tourneys = tourneys.filter(
            tournament_date__lte=datetime.strptime(to_date, "%m/%d/%Y")
        )

    tournament_table = TournamentTable(tourneys)
    RequestConfig(request, paginate={"per_page": 50}).configure(tournament_table)

    return render(
        request,
        "agagd_core/tournament_list.html",
        {
            "details": details,
            "from_date": from_date,
            "to_date": to_date,
            "tournament_table": tournament_table,
        },
    )


def game_stats(request):
    games_by_date = []

    for game_obj in Game.objects.values("game_date").annotate(Count("game_date")):
        try:
            game_date = datetime.strptime(str(game_obj["game_date"]), "%Y-%m-%d")
            games_by_date.append(
                {
                    "date": game_date.strftime("%Y-%m-%d"),
                    "count": game_obj["game_date__count"],
                }
            )
        except ValueError:
            pass

    sorted_games_by_date = sorted(games_by_date, key=lambda d: d["date"])
    return JsonResponse(sorted_games_by_date)


# AGAGD Pages
class InformationPageView(TemplateView):
    template_name = "information.html"


class QualificationsPageView(TemplateView):
    template_name = "qualifications.html"
