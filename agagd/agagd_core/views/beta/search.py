from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView


class SearchView(TemplateView):
    template_name = "beta.search_page.html"

    def get(self, request):
        query = request.GET.get("q", "")

        if not query:
            return render(request, self.template_name)

        if query.isdigit():
            member_id = [int(query)]
            return HttpResponseRedirect(reverse("member_detail", args=member_id))

        return HttpResponseRedirect(f"/search/?q={query}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Search -- Players | Games | Tournaments"

        return context
