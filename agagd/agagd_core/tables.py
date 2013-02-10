
import django_tables2 as tables
from agagd_core.models import Games

class GameTable(tables.Table):
    class Meta:
        model = Games
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}

