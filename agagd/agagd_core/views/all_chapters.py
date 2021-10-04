from agagd_core.models import Chapters
from agagd_core.tables.all_chapters_table import AllChaptersTable
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django_tables2.config import RequestConfig


class AllChaptersPageView(DetailView):
    template_name = "all_chapters_page.html"

    def get(self, request):
        chapters = Chapters.objects.values(
            "member_id", "name", "contact", "url", "meeting_text"
        )

        all_chapters_table = AllChaptersTable(chapters)
        RequestConfig(request, paginate={"per_page": 50}).configure(all_chapters_table)

        context = locals()
        context["all_chapters_table"] = all_chapters_table

        return TemplateResponse(request, self.template_name, context)
