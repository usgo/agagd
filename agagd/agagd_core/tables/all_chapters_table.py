import agagd_core.models as agagd_models
import django_tables2 as tables

# Base Bootstrap Column Header Attributes
default_bootstrap_header_column_attrs = {
    "class": "table",
    "thead": {"class": "thead-dark"},
    "th": {"scope": "col"},
}


class AllChaptersTable(tables.Table):
    class Meta:
        attrs = default_bootstrap_header_column_attrs
        model = agagd_models.Chapters
        template_name = "django_tables2/bootstrap4.html"
