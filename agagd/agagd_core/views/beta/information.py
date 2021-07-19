from django.views.generic import TemplateView


class InformationView(TemplateView):
    template_name = "beta.information.html"

    def get_context_data(self, **kwargs):
        context = super(InformationView, self).get_context_data(**kwargs)
        context["page_title"] = "Ratings Overview"

        return context
