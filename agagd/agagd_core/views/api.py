from datetime import datetime, timedelta

from agagd_core.json_response import JsonResponse
from agagd_core.models import Game, Member
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth, TruncWeek
from django.http import HttpResponse
from django.views import View


class ApiStatusView(View):
    def get(self, request):
        response = {"health_status_code": 200, "health_status": "The AGAGD is running."}
        return JsonResponse(response)


class ApiGameCountView(View):
    def get(self, request):
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


class ApiPlayerRatings(View):
    def __get_ratings_json(self, ratings_obj):
        ratings_json = []

        for rating in ratings_obj:
            elab_date = None
            sigma = None
            players_rating = None

            if isinstance(rating, dict):
                if "week_date" in rating:
                    elab_date = rating["week_date"]
                elif "month_date" in rating:
                    elab_date = rating["month_date"]
                sigma = rating["sigma__avg"]
                players_rating = rating["rating__avg"]
            else:
                elab_date = rating.elab_date
                sigma = rating.sigma
                players_rating = rating.rating

            if elab_date != None:
                ratings_json.append(
                    {"sigma": sigma, "elab_date": elab_date, "rating": players_rating}
                )
        return ratings_json

    def __get_less_current_date(self, number_of_weeks):
        return datetime.now() - timedelta(weeks=number_of_weeks)

    def get(self, request, *args, **kwargs):
        member_id = self.kwargs.get("player_id")
        time_period = self.kwargs.get("time_period")

        player = Member.objects.get(pk=member_id)

        ratings = None
        min_ratings = 5

        if time_period == 1:
            ratings = (
                player.ratings_set.all()
                .filter(elab_date__year__gte=self.__get_less_current_date(52).year)
                .order_by("elab_date")
            )
        elif time_period == 5:
            ratings = (
                player.ratings_set.all()
                .filter(elab_date__year__gte=self.__get_less_current_date(260).year)
                .annotate(week_date=TruncWeek("elab_date"))
                .values("week_date")
                .annotate(Avg("rating"), Avg("sigma"))
                .order_by("week_date")
            )
        elif time_period == 10:
            ratings = (
                player.ratings_set.all()
                .filter(elab_date__year__gte=self.__get_less_current_date(260).year)
                .annotate(month_date=TruncMonth("elab_date"))
                .values("month_date")
                .annotate(Avg("rating"), Avg("sigma"))
                .order_by("month_date")
            )

        if ratings == None or ratings.count() < min_ratings:
            return JsonResponse(
                {
                    "status": "not enough data",
                    "status_message": "Not enough data to produce a rating graph.",
                }
            )
        else:
            return JsonResponse(self.__get_ratings_json(ratings))

        return JsonResponse(
            {
                "status": "incorrect ratings page",
                "status_message": f"There is no data to be found for {member_id}.",
            }
        )
