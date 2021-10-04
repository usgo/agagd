import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import django_tables2 as tables
from agagd_core.models import Chapters
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html


class PlayersInformationTable(tables.Table):
    full_name = tables.Column()
    members_chapter_name = tables.Column(
        verbose_name="Chapter",
        linkify={"viewname": "chapter_detail", "args": [tables.A("chapter_id_id")]},
    )
    member_id = tables.Column()
    status = tables.Column()
    rating = tables.Column()
    renewal_due = tables.Column()

    class Meta:
        template_name = "player_profile_information.html"


class PlayersOpponentTable(tables.Table):
    opponent = tables.Column(
        orderable=False,
        linkify={
            "viewname": "players_profile",
            "args": [tables.A("opponent.member_id")],
        },
    )
    total = tables.Column(verbose_name="Games")
    won = tables.Column(verbose_name="Won", default=0)
    lost = tables.Column(verbose_name="Lost")
    ratio = tables.Column(verbose_name="Rate", default=0, empty_values=(-1,))

    def render_ratio(self, record):
        ratio = record["won"] / record["total"]

        return f"{ratio:.2f}"

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        orderable = False
        template_name = "django_tables2/bootstrap4.html"


class PlayersTournamentTable(tables.Table):
    tournament = tables.Column(
        linkify=("tournament_detail", [tables.A("tournament.pk")])
    )
    date = tables.Column(default="Unknown")
    won = tables.Column(verbose_name="Won", default=0)
    lost = tables.Column(verbose_name="Lost", default=0)

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = ("date", "tournament", "won", "lost")
        orderable = False
        template_name = "django_tables2/bootstrap4.html"
        sequence = fields
