import agagd_core.defaults.styles.django_tables2 as django_tables2_styles
import agagd_core.models as agagd_models
import django_tables2 as tables


class AllTournamentsTable(tables.Table):
    tournament_date = tables.Column(verbose_name="Date")
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
    city = tables.Column(attrs=django_tables2_styles.default_bootstrap_column_attrs)
    state = tables.Column(attrs=django_tables2_styles.default_bootstrap_column_attrs)
    total_players = tables.Column(
        attrs=django_tables2_styles.default_bootstrap_column_attrs
    )

    class Meta:
        attrs = django_tables2_styles.default_bootstrap_header_column_attrs
        fields = (
            "description",
            "tournament_code",
            "city",
            "state",
            "rounds",
            "total_players",
            "tournament_date",
            "elab_date",
        )
        model = agagd_models.Tournament
        orderable = False
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"
