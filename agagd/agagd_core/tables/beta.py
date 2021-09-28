# AGAGD Models Imports
import agagd_core.models as agagd_models

# DJango Imports
import django_tables2 as tables

# AGAGD Column Imports
from agagd_core.tables.core import ChapterColumn
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.safestring import mark_safe

# Base Bootstrap Column Attributes
default_bootstrap_column_attrs = {
    "th": {"class": "d-none d-lg-table-cell d-xl-table-cell"},
    "td": {"class": "d-none d-lg-table-cell d-xl-table-cell"},
}

# Base Bootstrap Column Header Attributes
default_bootstrap_header_column_attrs = {
    "class": "table",
    "thead": {"class": "thead-dark"},
    "th": {"scope": "col"},
}


class SearchResultsTable(tables.Table):
    member_id = tables.Column(linkify=("players_profile", [tables.A("member_id")]))
    chapter_id = ChapterColumn(verbose_name="Chapter")
    players__rating = tables.Column(verbose_name="Rating")
    country = tables.Column()
    full_name = tables.Column(linkify=("players_profile", [tables.A("member_id")]))

    class Meta:
        attrs = default_bootstrap_header_column_attrs
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
