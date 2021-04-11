# AGAGD Core Imports
from agagd_core.models import Chapters
from agagd_core.models import Game
from agagd_core.models import Member
from agagd_core.models import Tournament
from agagd_core.models import TopDan
from agagd_core.models import TopKyu
from agagd_core.models import MostTournamentsPastYear
from agagd_core.models import MostRatedGamesPastYear

# Django Imports
import django_tables2 as tables
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

class WinnerColumn(tables.Column):
    def __init__(
        self,
        color='W',
        viewname=None,
        urlconf=None,
        args=None,
        kwargs=None,
        current_app=None,
        attrs=None,
        **extra
    ):
        super().__init__(
            attrs=attrs,
            linkify=dict(
                viewname=viewname,
                urlconf=urlconf,
                args=args,
                kwargs=kwargs,
                current_app=current_app,
            ),
            **extra
        )
        self.color = color
    def render(self, value, record):
        if record.result == self.color:
            self.attrs['td'] = {'class': 'winner'} 
        else:
            self.attrs['td'] = {'class': 'runner-up'}
        return value

class ChapterColumn(tables.Column):
    # Takes a chapter ID and produces an href with the chapter's name
    def render(self, value):
        try:
            members_chapter = Chapters.objects.get(member_id=value)

            chapter_url = reverse(
                viewname='chapter_detail',
                kwargs={'chapter_id': value})

            chapter_name = members_chapter.name
            if chapter_name is None or chapter_name == "":
                chapter_name = members_chapter.code

            chapter_html = mark_safe("<a href='{}'>{}</a>".format(chapter_url, chapter_name))
        except:
            chapter_html = u"\u2014"

        return chapter_html

#Standard gameTable display as is on agagd.usgo.org and most pages
class GameTable(tables.Table):
    game_date = tables.Column(
        verbose_name="Date",
        attrs={
            "th": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            },
            "td": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            }
        }
    )
    handicap = tables.Column(
        attrs={
            "th": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            },
            "td": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            }
        }
    )
    pin_player_1 = WinnerColumn(color='W',
            viewname='member_detail',
            verbose_name="White",
            kwargs={"member_id":tables.A('pin_player_1.member_id')})
    pin_player_2 = WinnerColumn(color='B',
            viewname='member_detail',
            verbose_name="Black",
            kwargs={"member_id":tables.A('pin_player_2.member_id')})
    tournament_code = tables.LinkColumn(
            verbose_name="Tournament",
            viewname='tournament_detail',
            kwargs={'tourn_code':tables.A('tournament_code.tournament_code')})

    class Meta:
        model = Game
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            },
        }
        fields = (
            'game_date',
            'tournament_code',
            'pin_player_1',
            'pin_player_2',
            'round',
            'handicap',
            'komi'
        )
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"

# Alternative GameTable
#
# Displays GameTable without the Tournament Name Column
#
# References:
# GitHubIssue#20
class SecondaryGameTable(GameTable):
    tournament_code = None

    class Meta:
        model = Game
        fields = (
            'game_date',
            'round',
            'pin_player_1',
            'pin_player_2',
            'handicap',
            'komi'
        )
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"

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
        return "{:.2f}".format(record['won'] / record['total'])

    class Meta:
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        order_by = ('-total', '-won')
        template_name = "django_tables2/bootstrap4.html"

class MemberTable(tables.Table):
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={"member_id": tables.A('member_id')})
    chapter_id  = ChapterColumn(
        verbose_name="Chapter"
    )
    players__rating = tables.Column(
        verbose_name="Rating"
    )
    country = tables.LinkColumn(
        'country_detail',
        kwargs={"country_name": tables.A('country')})
    full_name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('member_id')})

    class Meta:
        model = Member
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        fields = ('full_name', 'state', 'players__rating', 'renewal_due', 'country')
        sequence = ('full_name', 'players__rating', 'chapter_id', 'country', 'state', 'renewal_due', 'member_id')
        template_name = "django_tables2/bootstrap4.html"

class ChapterMemberTable(MemberTable):
    class Meta:
        model = Member
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        fields = ('full_name', 'state', 'players__rating', 'renewal_due', 'country')
        sequence = ('full_name', 'players__rating', 'country', 'state', 'renewal_due', 'member_id')
        template_name = "django_tables2/bootstrap4.html"

class TopDanTable(tables.Table):
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={"member_id": tables.A('member_id')})
    full_name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('member_id')})
    class Meta:
        model = TopDan
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        fields = ('member_id', 'full_name', 'rating')
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"

class TopKyuTable(tables.Table):
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={"member_id": tables.A('member_id')})
    full_name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('member_id')})
    class Meta:
        model = TopKyu
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        fields = ('member_id', 'full_name', 'rating')
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"

class MostRatedGamesPastYearTable(tables.Table):
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={'member_id': tables.A('member_id')})
    name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('member_id')})
    class Meta:
        model = MostRatedGamesPastYear
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        fields = ('member_id', 'name', 'total')
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"

class MostTournamentsPastYearTable(tables.Table):
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={'member_id': tables.A('member_id')})
    name = tables.LinkColumn(
       'member_detail',
        kwargs={'member_id': tables.A('member_id')})
    class Meta:
        model = MostTournamentsPastYear
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        fields = ('member_id', 'name', 'total')
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"

class AllPlayerRatingsTable(tables.Table):
    full_name = tables.LinkColumn(
        'member_detail',
        kwargs={
            "member_id": tables.A('member_id')
        }
    )
    member_id = tables.LinkColumn(
        'member_detail',
        kwargs={
            "member_id": tables.A('member_id')
        }
    )
    type = tables.Column()
    players__rating = tables.Column()
    chapter_id = ChapterColumn(
        verbose_name="Chapter"
    )
    state = tables.Column()
    players__sigma = tables.Column(
        verbose_name="Sigma"
    )

    class Meta:
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        fields = (
                  'full_name',
                  'member_id',
                  'players__rating',
                  'players__sigma',
                  'type',
                  'chapter_id',
                  'state',
                 )
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"

class TournamentTable(tables.Table):
    tournament_date = tables.Column(
        verbose_name="Date",
        attrs={
            "th": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            },
            "td": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            }
        }
    )
    tournament_code = tables.LinkColumn(
            'tournament_detail',
            verbose_name="Code",
            kwargs={'tourn_code':tables.A('tournament_code')},)
    total_players = tables.Column(
        verbose_name="# Players",
        attrs={
            "th": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            },
            "td": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            }
        }
    )
    elab_date = tables.Column(
        verbose_name="Rated",
        attrs={
            "th": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            },
            "td": {
                "class": "d-none d-lg-table-cell d-xl-table-cell"
            }
        }
    )

    class Meta:
        model = Tournament
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            },
            "th": {
                "scope": "col"
            }
        }
        fields = ("tournament_date", "tournament_code", "description", "city", "state", "total_players", "rounds", 'elab_date')
        sequence = fields
        template_name = "django_tables2/bootstrap4.html"

class TournamentPlayedTable(tables.Table):
    tournament = tables.LinkColumn(
            'tournament_detail',
            kwargs={'tourn_code':tables.A('tournament.pk')},)
    date = tables.Column(default="Unknown")
    won = tables.Column(verbose_name="Won", default=0)
    lost = tables.Column(verbose_name="Lost", default=0) 
    #Steve note for issue #122 here

    class Meta:
        attrs = { 
            "class": "table", 
            "thead": {
                "class": "thead-light"
            }
        }
        template_name = "django_tables2/bootstrap4.html"
