import django_tables2 as tables
from agagd_core.models import Games, Members, Tournaments

class WinnerColumn(tables.LinkColumn):
    def __init__(self, color, *args, **kwargs):
        tables.LinkColumn.__init__(self, *args, **kwargs)
        self.color = color

    def render(self, value, record, bound_column):
        if record.result == self.color:
            self.attrs['td'] = {'class': 'winner'} 
        else:
            self.attrs['td'] = {'class': 'foo'}
        return tables.LinkColumn.render(self, value, record, bound_column)

class GameTable(tables.Table):
    pin_player_1 = WinnerColumn('W',
            viewname='agagd_core.views.member_detail',
            verbose_name="white player",
            kwargs={"member_id":tables.A('pin_player_1.member_id')})
    pin_player_2 = WinnerColumn('B',
            'agagd_core.views.member_detail', 
            verbose_name="black player",
            kwargs={"member_id":tables.A('pin_player_2.member_id')})
    tournament_code = tables.LinkColumn(
            verbose_name="Tournament",
            viewname='agagd_core.views.tournament_detail',
            kwargs={'tourn_code':tables.A('tournament_code.tournament_code')},)

    class Meta:
        model = Games
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("game_date", "round", "pin_player_1",
                "pin_player_2", 'handicap', 'tournament_code')
        sequence = fields

class OpponentTable(tables.Table):
    def __init__(self, qs, p1, *args, **kwargs):
        self.this_player = p1
        tables.Table.__init__(self, qs)

    empty_text = "Opponent information couldn't be calculated"
    opponent = tables.LinkColumn(
        'agagd_core.views.member_detail',
        kwargs={"member_id": tables.A('opponent.member_id')})
    total = tables.Column(verbose_name="Games")
    won = tables.Column(verbose_name="Won", default=0)
    lost = tables.Column(verbose_name="Lost")
    ratio = tables.Column(verbose_name="Rate", default=0, empty_values=(-1,), orderable=False)

    def render_ratio(self, record):
        print float(record['won']) / record['total']
        return "%0.2f" % (float(record['won']) / record['total'])

    class Meta:
        attrs = {"class": "paleblue"}
        order_by = ('-total', '-won')

class MemberTable(tables.Table):
    member_id = tables.LinkColumn(
            'agagd_core.views.member_detail',
            kwargs={"member_id":tables.A('member_id')})

    class Meta:
        model = Members
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("full_name", "state", "chapter", "join_date")
        sequence = fields

class TournamentTable(tables.Table):
    tournament_code = tables.LinkColumn(
            'agagd_core.views.tournament_detail',
            kwargs={'tourn_code':tables.A('tournament_code')},)
    elab_date = tables.Column(verbose_name="rated on")

    class Meta:
        model = Tournaments
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("tournament_code", "description", "tournament_date", "city", "state", "total_players", "rounds", 'elab_date')
        sequence = fields

class TournamentPlayedTable(tables.Table):
    tournament = tables.LinkColumn(
            'agagd_core.views.tournament_detail',
            kwargs={'tourn_code':tables.A('tournament.pk')},)
    date = tables.Column(default="Unknown")
    won = tables.Column(verbose_name="Won", default=0)
    lost = tables.Column(verbose_name="Lost", default=0) 

    class Meta:
        attrs = {"class": "paleblue"}
