import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import agagd_core.models as agagd_models
import django_tables2 as tables
from agagd_core.tables.games import LinkFullMembersNameColumn


class TournamentsTable(tables.Table):
    tournament_date = tables.Column(verbose_name="Date", orderable=False)
    description = tables.Column(
        verbose_name="Name",
        linkify=("tournament_detail", [tables.A("tournament_code")]),
    )
    tournament_code = tables.Column(
        verbose_name="Code",
        linkify=("tournament_detail", [tables.A("tournament_code")]),
    )
    total_players = tables.Column(
        verbose_name="# Players",
        attrs=django_tables2_styles.default_bootstrap_column_attrs,
    )
    elab_date = tables.Column(verbose_name="Rated")

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "description",
            "tournament_code",
            "total_players",
            "tournament_date",
            "elab_date",
        )
        model = agagd_models.Tournament
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"


class TournamentsInformationTable(tables.Table):
    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "tournament_code",
            "description",
            "tournament_date",
            "elab_date",
            "state",
        )
        model = agagd_models.Tournament
        orderable = False
        sequence = fields
        template_name = "tournament_detail_information.html"


class TournamentsGamesTable(tables.Table):
    pin_player_1 = LinkFullMembersNameColumn(
        color="W",
        verbose_name="White",
        viewname="players_profile",
        kwargs={"player_id": tables.A("pin_player_1")},
    )

    pin_player_2 = LinkFullMembersNameColumn(
        color="B",
        verbose_name="Black",
        viewname="players_profile",
        kwargs={"player_id": tables.A("pin_player_2")},
    )

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = ("game_date", "pin_player_1", "pin_player_2", "handicap", "komi")
        model = agagd_models.Tournament
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
