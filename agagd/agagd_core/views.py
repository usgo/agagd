# Create your views here.  

from django.template import Context, loader
from django.shortcuts import render_to_response, render
from agagd_core.models import Games, Members
from agagd_core.tables import GameTable
from django.http import HttpResponse
from django.db.models import Q
from django_tables2   import RequestConfig
from datetime import datetime, timedelta



def index(request):
    game_list = Games.objects.filter(game_date__gte=datetime.now() - timedelta(days=180)).order_by('-game_date')
    print game_list.query
    table = GameTable(game_list)
    RequestConfig(request).configure(table)
    return render(request, "agagd_core/index.html",
            {
                'table': table,
            })

def member_detail(request, member_id):
    game_list = Games.objects.filter(
            Q(pin_player_1__exact=member_id) | Q(pin_player_2__exact=member_id)
            ).order_by('-game_date')
    player = Members.objects.get(member_id=member_id)
    table = GameTable(game_list)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, 'agagd_core/member.html',
            {
                'table': table,
                'player': player,
            }) 

def member_vs(request, member_id, other_id):
    game_list = Games.objects.filter(
            Q(pin_player_1__exact=member_id, pin_player_2__exact=other_id) |
            Q(pin_player_1__exact=other_id, pin_player_2__exact=member_id),
            ).order_by('-game_date')
    table = GameTable(game_list)
    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render_to_response('agagd_core/member.html',
            {
                'table': table,
            }) 

