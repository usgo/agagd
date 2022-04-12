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


def class_white(record):
    """returns td class for player 1 (white)"""
    return "winner" if record["result"] == "W" else "runner-up"


def class_black(record):
    """returns td class for player 2 (black)"""
    return "winner" if record["result"] == "B" else "runner-up"


class TournamentsGamesTable(tables.Table):
    white = tables.Column(
        linkify=("players_profile", [tables.A("white")]),
        attrs={"td": {"class": class_white}},
    )
    black = tables.Column(
        verbose_name="Black",
        linkify=("players_profile", [tables.A("black")]),
        attrs={"td": {"class": class_black}},
    )

    def render_white(self, record):
        name = record["white_name"]
        pin = record["white"]
        return f"{name} ({pin})"

    def render_black(self, record):
        name = record["black_name"]
        pin = record["black"]
        return f"{name} ({pin})"

    def render_result(self, value):
        if value == "W":
            return "White Wins"
        if value == "B":
            return "Black Wins"
        return "Draw"

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "date",
            "white",
            "black",
            "handicap",
            "komi",
            "result",
        )
        model = agagd_models.Tournament
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
