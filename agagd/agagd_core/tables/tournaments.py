import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import agagd_core.models as agagd_models
import django_tables2 as tables


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


def class_player_1(record):
    """returns td class for player 1 (white)"""
    return "winner" if record["result"] == "W" else "runner-up"


def class_player_2(record):
    """returns td class for player 2 (black)"""
    return "winner" if record["result"] == "B" else "runner-up"


class TournamentsGamesTable(tables.Table):
    full_name_and_id_1 = tables.Column(
        verbose_name="White",
        linkify=("players_profile", [tables.A("pin_player_1")]),
        attrs={"td": {"class": class_player_1}},
    )
    full_name_and_id_2 = tables.Column(
        verbose_name="Black",
        linkify=("players_profile", [tables.A("pin_player_2")]),
        attrs={"td": {"class": class_player_2}},
    )

    def render_result(self, value):
        if value == "W":
            return "White Wins"
        if value == "B":
            return "Black Wins"
        return "Draw"

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "game_date",
            "full_name_and_id_1",
            "full_name_and_id_2",
            "handicap",
            "komi",
            "result",
        )
        model = agagd_models.Tournament
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
