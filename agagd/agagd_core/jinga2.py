import agagd_core.models as agagd_models
from django.core.exceptions import ObjectDoesNotExist
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def get_members_name_and_id(value):
    """
        Provides jinja2 custom filter which returns
        the members information as
        "[member's full name] (member_id)".
    """
    try:
        member = agagd_models.Member.objects.values("full_name", "member_id").get(
            pk=value
        )
    except ObjectDoesNotExist:
        raise ("Member {value} does not exist.")

    return f"{member['full_name']} ({member['member_id']})"


def environment(**options):
    env = Environment(**options)
    env.filters["get_members_name_and_id"] = get_members_name_and_id
    env.globals.update({"static": static, "url": reverse})
    return env
