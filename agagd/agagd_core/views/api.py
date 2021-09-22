from agagd_core.json_response import JsonResponse
from django.http import HttpResponse
from django.views import View


class ApiStatusView(View):
    def get(self, request):
        response = {"health_status_code": 200, "health_status": "The AGAGD is running."}
        return JsonResponse(response)
