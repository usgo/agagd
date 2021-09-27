import agagd_core.models as agagd_models
import django_tables2 as tables
from django.utils.html import format_html

# Base Bootstrap Column Header Attributes
default_bootstrap_header_column_attrs = {
    "class": "table",
    "thead": {"class": "thead-dark"},
    "th": {"scope": "col"},
}


class AllChaptersTable(tables.Table):
    name = tables.Column(linkify=("chapter_detail", [tables.A("member_id")]))
    url = tables.Column()

    def render_url(self, value):
        return format_html("<a href='//{}' rel='external'>{}</a>", value, value)

    class Meta:
        attrs = default_bootstrap_header_column_attrs
        fields = ("name", "contact", "meeting_text", "url")
        model = agagd_models.Chapters
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
