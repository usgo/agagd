from datetime import datetime

from agagd_core.json_response import JsonResponse
from agagd_core.models import Game
from django.db.models import Count
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
