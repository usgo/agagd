# Create your views here.  

from django.template import Context, loader
from django.shortcuts import render_to_response, render
from agagd_core.models import Games
from agagd_core.tables import GameTable
from django.http import HttpResponse
from django.db.models import Q
from django_tables2   import RequestConfig



def index(request):
    return HttpResponse("foo")

def member_detail(request, member_id):
    game_list = Games.objects.filter(
            Q(pin_player_1__exact=member_id) | Q(pin_player_2__exact=member_id)
            ).order_by('-game_date')
    table = GameTable(game_list)
    RequestConfig(request).configure(table)
    return render(request, 'agagd_core/member.html',
            {
                'game_list': game_list,
                'table': table,
            }) 

def member_vs(request, member_id, other_id):
    game_list = Games.objects.filter(
            Q(pin_player_1__exact=member_id, pin_player_2__exact=other_id) |
            Q(pin_player_1__exact=other_id, pin_player_2__exact=member_id),
            ).order_by('-game_date')
    table = GameTable(game_list)
    RequestConfig(request).configure(table)
    return render_to_response('agagd_core/member.html',
            {
                'game_list': game_list,
                'table': table,
            }) 

