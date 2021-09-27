import agagd_core.models as agagd_models
import django_tables2 as tables

default_bootstrap_header_column_attrs = {
    "class": "table",
    "thead": {"class": "thead-dark"},
    "th": {"scope": "col"},
}


class TopDanTable(tables.Table):
    pin_player = tables.Column(
        orderable=False,
        linkify={
            "viewname": "players_profile",
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


class TopKyuTable(tables.Table):
    pin_player = tables.Column(
        orderable=False,
        linkify={
            "viewname": "players_profile",
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
