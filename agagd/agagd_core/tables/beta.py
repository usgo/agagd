# AGAGD Models Imports
import agagd_core.models as agagd_models

# DJango Imports
import django_tables2 as tables
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

# Column for the Winner of the Game
class LinkFullMembersNameColumn(tables.Column):
    def __init__(
        self,
        color="W",
        viewname=None,
        urlconf=None,
        args=None,
        kwargs=None,
        current_app=None,
        attrs=None,
        **extra,
    ):
        super().__init__(
            attrs=attrs,
            linkify=dict(
                viewname=viewname,
                urlconf=urlconf,
                args=args,
                kwargs=kwargs,
                current_app=current_app,
            ),
            **extra,
        )
        self.color = color

    def render(self, value, record):
        if record["result"] == self.color:
            self.attrs["td"] = {"class": "winner"}
        elif record["result"] != self.color:
            self.attrs["td"] = {"class": "runner-up"}

        try:
            member_name_and_id = agagd_models.Member.objects.get(member_id=value)
            value = f"{member_name_and_id.full_name} ({value})"
        except ObjectDoesNotExist:
            value = None

        return value


# Basic table which is use as as base for many of the game layouts.
class GamesTable(tables.Table):
    game_date = tables.Column(
        verbose_name="Date", attrs=default_bootstrap_column_attrs, orderable=False
    )
    handicap = tables.Column(attrs=default_bootstrap_column_attrs, orderable=False)
    pin_player_1 = LinkFullMembersNameColumn(
        color="W",
        viewname="beta:players_profile",
        verbose_name="White",
        kwargs={"player_id": tables.A("pin_player_1")},
        orderable=False,
    )
    pin_player_2 = LinkFullMembersNameColumn(
        color="B",
        viewname="beta:players_profile",
        verbose_name="Black",
        kwargs={"player_id": tables.A("pin_player_2")},
        orderable=False,
    )
    tournament_code = tables.LinkColumn(
        verbose_name="Tournament",
        viewname="tournament_detail",
        kwargs={"tourn_code": tables.A("tournament_code")},
        orderable=False,
    )

    class Meta:
        model = agagd_models.Game
        fields = (
            "game_date",
            "handicap",
            "pin_player_1",
            "pin_player_2",
            "tournament_code",
        )
        sequence = fields
        attrs = default_bootstrap_header_column_attrs
        template_name = "django_tables2/bootstrap4.html"


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
            "viewname": "beta:players_profile",
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


class TournamentsTable(tables.Table):
    tournament_date = tables.Column(
        verbose_name="Date", attrs=default_bootstrap_column_attrs, orderable=False
    )
    description = tables.LinkColumn(
        "tournament_detail",
        verbose_name="Name",
        kwargs={"tourn_code": tables.A("tournament_code")},
        orderable=False,
    )
    total_players = tables.Column(
        verbose_name="# Players", attrs=default_bootstrap_column_attrs, orderable=False
    )
    elab_date = tables.Column(
        verbose_name="Rated", attrs=default_bootstrap_column_attrs, orderable=False
    )

    class Meta:
        model = agagd_models.Tournament
        fields = ("tournament_date", "description", "total_players", "elab_date")
        sequence = fields
        attrs = default_bootstrap_header_column_attrs
        template_name = "django_tables2/bootstrap4.html"


class PlayersTournamentTable(tables.Table):
    tournament = tables.LinkColumn(
        "tournament_detail",
        kwargs={"tourn_code": tables.A("tournament.pk")},
        orderable=False,
    )
    date = tables.Column(orderable=False, default="Unknown")
    won = tables.Column(orderable=False, verbose_name="Won", default=0)
    lost = tables.Column(orderable=False, verbose_name="Lost", default=0)

    class Meta:
        fields = ("date", "tournament", "won", "lost")
        sequence = fields
        attrs = default_bootstrap_header_column_attrs
        template_name = "django_tables2/bootstrap4.html"


class Top10DanTable(tables.Table):
    pin_player = tables.Column(
        orderable=False,
        linkify={
            "viewname": "beta:players_profile",
            "args": [tables.A("pin_player.member_id")],
        },
    )
    sigma = tables.Column(orderable=False)
    rating = tables.Column(orderable=False)

    def render_pin_player(self, value):
        try:
            member_name_and_id = agagd_models.Member.objects.values(
                "full_name", "member_id"
            ).get(member_id=value.member_id)
            value = f"{value}"
        except ObjectDoesNotExist:
            value = None

        return value

    class Meta:
        model = agagd_models.Players
        fields = ("pin_player", "sigma", "rating")
        sequence = fields
        attrs = default_bootstrap_header_column_attrs
        template_name = "django_tables2/bootstrap4.html"


class Top10KyuTable(tables.Table):
    pin_player = tables.Column(
        orderable=False,
        linkify={
            "viewname": "beta:players_profile",
            "args": [tables.A("pin_player.member_id")],
        },
    )
    sigma = tables.Column(orderable=False)
    rating = tables.Column(orderable=False)

    def render_pin_player(self, value):
        try:
            member_name_and_id = agagd_models.Member.objects.values(
                "full_name", "member_id"
            ).get(member_id=value.member_id)
            value = f"{value}"
        except ObjectDoesNotExist:
            value = None

        return value

    class Meta:
        model = agagd_models.Players
        fields = ("pin_player", "sigma", "rating")
        sequence = fields
        attrs = default_bootstrap_header_column_attrs
        template_name = "django_tables2/bootstrap4.html"
