import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import agagd_core.models as agagd_models
import django_tables2 as tables
from agagd_core.tables.core import ChapterColumn


class SearchResultsTable(tables.Table):
    member_id = tables.Column(linkify=("players_profile", [tables.A("member_id")]))
    chapter_id = ChapterColumn(verbose_name="Chapter")
    players__rating = tables.Column(verbose_name="Rating")
    country = tables.Column()
    full_name = tables.Column(linkify=("players_profile", [tables.A("member_id")]))

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "full_name",
            "member_id",
            "players__rating",
            "chapter_id",
            "country",
            "state",
            "renewal_due",
        )
        model = agagd_models.Member
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
