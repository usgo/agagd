from django.views.generic import TemplateView


class SearchPageView(TemplateView):
    template_name = "beta.search_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Search -- Players | Games | Tournaments"

        return context
