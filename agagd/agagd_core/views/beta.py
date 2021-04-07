from datetime import datetime
from datetime import timedelta
from datetime import date
from agagd_core.models import Game
from agagd_core.models import Member
from agagd_core.models import Tournament
from agagd_core.models import TopDan
from agagd_core.models import TopKyu
from agagd_core.models import MostRatedGamesPastYear
from agagd_core.models import MostTournamentsPastYear
from agagd_core.models import Chapters
from agagd_core.models import Country
from agagd_core.tables.beta import GameTable
from agagd_core.tables.beta import SecondaryGameTable
from agagd_core.tables.beta import MemberTable
from agagd_core.tables.beta import ChapterMemberTable
from agagd_core.tables.beta import TournamentTable
from agagd_core.tables.beta import OpponentTable
from agagd_core.tables.beta import TournamentPlayedTable
from agagd_core.tables.beta import TopDanTable
from agagd_core.tables.beta import TopKyuTable
from agagd_core.tables.beta import AllPlayerRatingsTable
from agagd_core.tables.beta import MostRatedGamesPastYearTable
from agagd_core.tables.beta import MostTournamentsPastYearTable
from django.shortcuts import render
from django.shortcuts import get_object_or_404 
from django.shortcuts import redirect
from django_tables2 import RequestConfig

def index(request):
    game_list = Game.objects.filter(game_date__gte=datetime.now() - timedelta(days=180)).order_by('-game_date')
    table = GameTable(game_list, prefix='games')
    topDanList = TopDan.objects.values()
    topDanTable = TopDanTable(topDanList)
    topKyuList = TopKyu.objects.values()
    topKyuTable = TopKyuTable(topKyuList)
    mostRatedGamesPastYearList = MostRatedGamesPastYear.objects.values()
    mostRatedGamesTable = MostRatedGamesPastYearTable(mostRatedGamesPastYearList)
    mostTournamentsPastYearList = MostTournamentsPastYear.objects.values()
    mostTournamentsPastYearTable = MostTournamentsPastYearTable(mostTournamentsPastYearList)
    RequestConfig(request).configure(table)
    tourneys = Tournament.objects.all().order_by('-tournament_date')
    t_table= TournamentTable(tourneys, prefix='tourneys')
    RequestConfig(request, paginate={'per_page': 10}).configure(t_table)

    return render(request, 'agagd_core/index.beta.html',
            {
                'table': table,
                'top_dan_table': topDanTable,
                'top_kyu_table': topKyuTable,
                'most_rated_games_table': mostRatedGamesTable,
                'most_tournaments_table': mostTournamentsPastYearTable,
                'tournaments': t_table,
            })

