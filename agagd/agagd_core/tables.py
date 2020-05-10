import django_tables2 as tables
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from agagd_core.models import Chapters, Game, Member, Tournament, TopDan, TopKyu, MostTournamentsPastYear, MostRatedGamesPastYear

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

#Standard gameTable display as is on agagd.usgo.org and most pages
class GameTable(tables.Table):
    pin_player_1 = WinnerColumn('W',
            viewname='member_detail',
            verbose_name="white player",
            kwargs={"member_id":tables.A('pin_player_1.member_id')})
    pin_player_2 = WinnerColumn('B',
            viewname='member_detail', 
            verbose_name="black player",
            kwargs={"member_id":tables.A('pin_player_2.member_id')})
    tournament_code = tables.LinkColumn(
            verbose_name="Tournament",
            viewname='tournament_detail',
            kwargs={'tourn_code':tables.A('tournament_code.tournament_code')},)

    class Meta:
        model = Game
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("game_date", "round", "pin_player_1",
                "pin_player_2", 'handicap', 'komi', 'tournament_code')
        sequence = fields

#Modified gaeTable to remove duplicate tournament listing displayed on the page, GitHubIssue#20
class GameTable2(tables.Table):
    pin_player_1 = WinnerColumn('W',
            viewname='member_detail',
            verbose_name="white player",
            kwargs={"member_id":tables.A('pin_player_1.member_id')})
    pin_player_2 = WinnerColumn('B',
            'member_detail', 
            verbose_name="black player",
            kwargs={"member_id":tables.A('pin_player_2.member_id')})
    class Meta:
        model = Game
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("game_date", "round", "pin_player_1",
                "pin_player_2", 'handicap', 'komi')
        sequence = fields



class OpponentTable(tables.Table):
    def __init__(self, qs, p1, *args, **kwargs):
        self.this_player = p1
        tables.Table.__init__(self, qs)

    empty_text = "Opponent information couldn't be calculated"
    opponent = tables.LinkColumn(
        'member_detail',
        kwargs={"member_id": tables.A('opponent.member_id')})
    total = tables.Column(verbose_name="Games")
    won = tables.Column(verbose_name="Won", default=0)
    lost = tables.Column(verbose_name="Lost")
    ratio = tables.Column(verbose_name="Rate", default=0, empty_values=(-1,), orderable=False)

    def render_ratio(self, record):
        return "%0.2f" % (float(record['won']) / record['total'])

    class Meta:
        attrs = {"class": "paleblue"}
        order_by = ('-total', '-won')

class MemberTable(tables.Table):
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={"member_id": tables.A('member_id')})
    chapter_id  = tables.Column(
        verbose_name="Chapters"
    )
    country = tables.LinkColumn(
        'country_detail',
        kwargs={"country_name": tables.A('country')})
    full_name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('member_id')})

    def render_chapter_id(self, value):
        try:
            members_chapter = Chapters.objects.get(member_id=value)
            chapter_url = reverse(
                viewname='agagd_core.views.chapter_detail',
                kwargs={'chapter_code': members_chapter.code})
            chapter_html = mark_safe("<a href='{}'>{}</a>".format(chapter_url, members_chapter.code))
        except:
            chapter_html = u"\u2014"
        return chapter_html

    class Meta:
        model = Member
        attrs = {"class": "paleblue"}
        fields = ('full_name', 'state', 'join_date', 'country')
        sequence = ('full_name', 'chapter_id', 'country', 'state', 'join_date', 'member_id')

class TopDanTable(tables.Table):
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={"member_id": tables.A('member_id')})
    full_name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('member_id')})
    class Meta:
        model = TopDan
        attrs = {"class": "paleblue"}
        fields = ('member_id', 'full_name', 'rating')
        sequence = fields

class TopKyuTable(tables.Table):
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={"member_id": tables.A('member_id')})
    full_name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('member_id')})
    class Meta:
        model = TopKyu
        attrs = {"class": "paleblue"}
        fields = ('member_id', 'full_name', 'rating')
        sequence = fields

class MostRatedGamesPastYearTable(tables.Table):
    pin = tables.LinkColumn(
        'member_detail',
        kwargs={'member_id': tables.A('pin')})
    name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('pin')})
    class Meta:
        model = MostRatedGamesPastYear
        attrs = {"class": "paleblue"}
        fields = ('pin', 'name', 'total')
        sequence = fields

class MostTournamentsPastYearTable(tables.Table):
    pin = tables.LinkColumn(
        'member_detail',
        kwargs={'member_id': tables.A('pin')})
    name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('pin')})
    class Meta:
        model = MostTournamentsPastYear
        attrs = {"class": "paleblue"}
        fields = ('pin', 'name', 'total')
        sequence = fields


class TournamentTable(tables.Table):
    tournament_code = tables.LinkColumn(
            'tournament_detail',
            kwargs={'tourn_code':tables.A('tournament_code')},)
    elab_date = tables.Column(verbose_name="rated on")

    class Meta:
        model = Tournament
        attrs = {"class": "paleblue"}
        fields = ("tournament_code", "description", "tournament_date", "city", "state", "total_players", "rounds", 'elab_date')
        sequence = fields

class TournamentPlayedTable(tables.Table):
    tournament = tables.LinkColumn(
            'tournament_detail',
            kwargs={'tourn_code':tables.A('tournament.pk')},)
    date = tables.Column(default="Unknown")
    won = tables.Column(verbose_name="Won", default=0)
    lost = tables.Column(verbose_name="Lost", default=0) 

    class Meta:
        attrs = {"class": "paleblue"}
