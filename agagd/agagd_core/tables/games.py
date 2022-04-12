import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import agagd_core.models as agagd_models
import django_tables2 as tables


def class_white(record):
    """returns td class for white"""
    return "winner" if record["result"] == "W" else "runner-up"


def class_black(record):
    """returns td class for black"""
    return "winner" if record["result"] == "B" else "runner-up"


# Basic table which is use as as base for many of the game layouts.
class GamesTable(tables.Table):
    white = tables.Column(
        linkify=("players_profile", [tables.A("white")]),
        attrs={"td": {"class": class_white}},
    )
    black = tables.Column(
        linkify=("players_profile", [tables.A("black")]),
        attrs={"td": {"class": class_black}},
    )
    tournament = tables.Column(
        verbose_name="Tournament",
        linkify=("tournament_detail", [tables.A("tournament")]),
    )

    def render_white(self, record):
        name = record["white_name"]
        pin = record["white"]
        return f"{name} ({pin})"

    def render_black(self, record):
        name = record["black_name"]
        pin = record["black"]
        return f"{name} ({pin})"

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "date",
            "white",
            "black",
            "tournament",
            "handicap",
        )
        model = agagd_models.Game
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
