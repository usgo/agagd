from django.views.generic import TemplateView


class RatingsOverviewPageView(TemplateView):
    template_name = "ratings_overview_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Ratings Overview"

        return context
