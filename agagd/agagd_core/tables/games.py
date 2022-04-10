import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import agagd_core.models as agagd_models
import django_tables2 as tables


def class_player_1(record):
    """returns td class for player 1 (white)"""
    return "winner" if record["result"] == "W" else "runner-up"


def class_player_2(record):
    """returns td class for player 2 (black)"""
    return "winner" if record["result"] == "B" else "runner-up"


# Basic table which is use as as base for many of the game layouts.
class GamesTable(tables.Table):
    game_date = tables.Column(
        verbose_name="Date", attrs=django_tables2_styles.default_bootstrap_column_attrs
    )
    handicap = tables.Column(
        attrs=django_tables2_styles.default_bootstrap_column_attrs, orderable=False
    )
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
    tournament_code = tables.Column(
        verbose_name="Tournament",
        linkify=("tournament_detail", [tables.A("tournament_code")]),
    )

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "full_name_and_id_1",
            "full_name_and_id_2",
            "tournament_code",
            "handicap",
            "game_date",
        )
        model = agagd_models.Game
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
