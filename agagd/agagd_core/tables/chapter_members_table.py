from agagd_core.models import Member
from agagd_core.tables.core import MemberTable

default_bootstrap_header_column_attrs = {
    "class": "table",
    "thead": {"class": "thead-dark"},
    "th": {"scope": "col"},
}


class ChapterMembersTable(MemberTable):
    class Meta:
        attrs = default_bootstrap_header_column_attrs
        fields = ("full_name", "state", "players__rating", "renewal_due", "country")
        model = Member
        orderable = False
        sequence = (
            "full_name",
            "players__rating",
            "country",
            "state",
            "renewal_due",
            "member_id",
        )
        template_name = "django_tables2/bootstrap4.html"
