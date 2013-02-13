
import django_tables2 as tables
from agagd_core.models import Games, Members

class GameTable(tables.Table):
    pin_player_1 = tables.LinkColumn(
            'agagd_core.views.member_detail',
            kwargs={"member_id":tables.A('pin_player_1.member_id')})
    pin_player_2 = tables.LinkColumn(
            'agagd_core.views.member_detail', 
            kwargs={"member_id":tables.A('pin_player_2.member_id')})
    class Meta:
        model = Games
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("game_date", "tournament_code", "round", 
                "pin_player_1", "color_1", "pin_player_2", "color_2", "result")
        sequence = fields

class MemberTable(tables.Table):
    member_id = tables.LinkColumn(
            'agagd_core.views.member_detail',
            kwargs={"member_id":tables.A('member_id')})
    class Meta:
        model = Members
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("full_name", "state", "chapter", )
        sequence = fields
