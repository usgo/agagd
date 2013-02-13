# Create your views here.  

from django.template import loader, RequestContext
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf 

from agagd_core.models import Games, Members
from agagd_core.tables import GameTable
from django.http import HttpResponseRedirect
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

#no idea what the right pattern is here; if the request has a member_id param, redirect
#to the member_detail page with that value.  Otherwise, i guess we send them home?
def member_fetch(request):
    context = RequestContext(request)
    if request.method != 'POST':
        return HttpResponseRedirect('/gd/')

    if 'member_id' in request.POST:
        return HttpResponseRedirect(
                    reverse('agagd_core.views.member_detail',
                    args=(request.POST['member_id'],))
                    )


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
                'num_games': len(game_list)
            }) 

def member_search_form(request):
    return render_to_response('agagd_core/search_form.html')

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

def tournament_detail(request):
    pass

def tournament_list(request):
    pass

