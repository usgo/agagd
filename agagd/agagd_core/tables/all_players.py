import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import agagd_core.models as agagd_models
import django_tables2 as tables


class AllPlayersTable(tables.Table):
    full_name = tables.Column(
        verbose_name="Name", linkify=("players_profile", [tables.A("member_id")])
    )
    chapter_id__name = tables.Column(
        verbose_name="Chapter Name",
        linkify=("chapter_detail", [tables.A("chapter_id")]),
    )
    state = tables.Column(attrs=django_tables2_styles.default_bootstrap_column_attrs)
    type = tables.Column(attrs=django_tables2_styles.default_bootstrap_column_attrs)
    players__sigma = tables.Column(
        attrs=django_tables2_styles.default_bootstrap_column_attrs
    )
    players__rating = tables.Column(verbose_name="Rating")

    def render_full_name(self, record):
        return f"{record['full_name']} ({record['member_id']})"

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "full_name",
            "players__rating",
            "players__sigma",
            "type",
            "chapter_id__name",
            "state",
        )
        model = agagd_models.Players
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
