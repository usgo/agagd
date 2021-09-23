from django.views.generic import TemplateView


class QualificationsPageView(TemplateView):
    template_name = "beta.qualifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "How to Submit Rated Games"

        return context
