import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import agagd_core.models as agagd_models
import django_tables2 as tables


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
            member_name_and_id = agagd_models.Member.objects.values("full_name").get(
                member_id=value
            )
            value = f"{member_name_and_id['full_name']} ({value})"
        except ObjectDoesNotExist:
            value = None

        return value


# Basic table which is use as as base for many of the game layouts.
class GamesTable(tables.Table):
    game_date = tables.Column(
        verbose_name="Date", attrs=django_tables2_styles.default_bootstrap_column_attrs
    )
    handicap = tables.Column(
        attrs=django_tables2_styles.default_bootstrap_column_attrs, orderable=False
    )
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
    tournament_code = tables.Column(
        verbose_name="Tournament",
        linkify=("tournament_detail", [tables.A("tournament_code")]),
    )

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "pin_player_1",
            "pin_player_2",
            "tournament_code",
            "handicap",
            "game_date",
        )
        model = agagd_models.Game
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
