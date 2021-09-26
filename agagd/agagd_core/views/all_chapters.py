from agagd_core.models import Chapters
from agagd_core.tables.all_chapters_table import AllChaptersTable
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView


class AllChaptersPageView(DetailView):
    template_name = "all_chapters_page.html"

    def get(self, request):
        chapters = Chapters.objects.all()

        all_chapters_table = AllChaptersTable(chapters)

        context = locals()
        context["all_chapters_table"] = all_chapters_table

        return TemplateResponse(request, self.template_name, context)
