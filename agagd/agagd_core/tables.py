
import django_tables2 as tables
from agagd_core.models import Games

class GameTable(tables.Table):
    class Meta:
        model = Games
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        sequence = ("game_date", "tournament_code", "round", "pin_player_1", "color_1", "pin_player_2", "color_2", "result")
        fields = sequence


