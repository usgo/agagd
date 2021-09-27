from agagd_core.models import Chapters, Member
from agagd_core.tables.chapter_information_table import ChapterInformationTable
from agagd_core.tables.chapter_members_table import ChapterMembersTable
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig


class ChaptersProfilePageView(DetailView):
    template_name = "chapter_profile_page.html"

    def get(self, request, *args, **kwargs):
        chapter_id = self.kwargs.get("chapter_id")
        chapter = get_object_or_404(Chapters, member_id=chapter_id)
        chapter_members = (
            Member.objects.filter(chapter_id=chapter_id)
            .values(
                "member_id",
                "chapter_id",
                "renewal_due",
                "state",
                "players__rating",
                "country",
                "full_name",
                "family_name",
            )
            .order_by("family_name")
        )

        chapter_information_table = ChapterInformationTable([chapter.__dict__])
        chapter_members_table = ChapterMembersTable(chapter_members)

        RequestConfig(request, paginate={"per_page": 25}).configure(
            chapter_members_table
        )

        context = locals()
        context["chapter_information_table"] = chapter_information_table
        context["chapter_members_table"] = chapter_members_table

        return TemplateResponse(request, self.template_name, context)
