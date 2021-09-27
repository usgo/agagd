import django_tables2 as tables
from django.views.generic.detail import DetailView


class ChapterInformationTable(tables.Table):
    member_id = tables.Column()
    name = tables.Column()
    contact = tables.Column()
    url = tables.Column()
    meeting_city = tables.Column()
    meeting_text = tables.Column()

    class Meta:
        template_name = "chapter_profile_info_django_tables2.html"
