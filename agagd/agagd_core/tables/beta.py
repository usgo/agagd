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


class PlayersInformationTable(tables.Table):
    full_name = tables.Column()
    member_id = tables.Column()
    status = tables.Column()
    rating = tables.Column()
    renewal_due = tables.Column()

    class Meta:
        template_name = "beta.player_profile_information.html"


class PlayersOpponentTable(tables.Table):
    opponent = tables.Column(
        orderable=False,
        linkify={
            "viewname": "players_profile",
            "args": [tables.A("opponent.member_id")],
        },
    )
    total = tables.Column(orderable=False, verbose_name="Games")
    won = tables.Column(orderable=False, verbose_name="Won", default=0)
    lost = tables.Column(orderable=False, verbose_name="Lost")
    ratio = tables.Column(
        verbose_name="Rate", default=0, empty_values=(-1,), orderable=False
    )

    def render_ratio(self, record):
        ratio = record["won"] / record["total"]

        return f"{ratio:.2f}"

    class Meta:
        attrs = default_bootstrap_header_column_attrs
        template_name = "django_tables2/bootstrap4.html"


class PlayersTournamentTable(tables.Table):
    tournament = tables.LinkColumn(
        "tournament_detail", kwargs={"code": tables.A("tournament.pk")}, orderable=False
    )
    date = tables.Column(orderable=False, default="Unknown")
    won = tables.Column(orderable=False, verbose_name="Won", default=0)
    lost = tables.Column(orderable=False, verbose_name="Lost", default=0)

    class Meta:
        fields = ("date", "tournament", "won", "lost")
        sequence = fields
        attrs = default_bootstrap_header_column_attrs
        template_name = "django_tables2/bootstrap4.html"


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
