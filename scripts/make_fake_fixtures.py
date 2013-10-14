# A simple script to generate fake data
import sys, random, json

USAGE = 'Usage: python make_fake_fixtures.py [num_of_members] [num_of_games] [num_of_tournaments]'
GIVEN_NAMES = [ 'bruce', 'malcolm', 'kobe', 'peter', 'kaylee', 'inara', ]
LAST_NAMES = [ 'lee', 'reynolds', 'bryant', 'parker', 'frye', 'serra', ]
CHAPTER_CODES = ['FFLY', 'NBAG', 'DEAD', 'BEEF']

import datetime as dt

if len(sys.argv) != 4:
    print USAGE
    quit()

try:
    member_count = int(sys.argv[1])
    game_count = int(sys.argv[2])
    tourney_count = int(sys.argv[3])
except ValueError:
    print USAGE
    quit()

members = []
for member_id in range(member_count):
    first_name = random.choice(GIVEN_NAMES)
    last_name = random.choice(LAST_NAMES)
    members.append({
        'pk': member_id,
        'model': 'agagd_core.member',
        'fields': {
            'member_id': member_id,
            'legacy_id': '',
            'full_name': '%s %s' % (first_name, last_name),
            'given_names': first_name,
            'family_name': last_name,
            'join_date': None,
            'city': 'Seattle',
            'state': 'WA',
            'region': 'some region',
            'country': random.choice(['USA', 'CAN', 'JPN', 'KOR', 'CHN', 'TWN']),
            'chapter': random.choice(CHAPTER_CODES),
            'chapter_id': 'MAYBE_FK',
            'occupation': '',
            'citizen': 'yes',
            'password': 'hallo!',
            'last_changed': None
        }
    })

tournaments = []
for tourney_id in range(tourney_count):
    tournaments.append({
        'pk': 'T%s' % str(tourney_id),
        'model': 'agagd_core.tournament',
        'fields': {
            'total_players': random.randint(4,20),
            'city': '',
            'elab_date': '2013-07-01',
            'description': '',
            'wall_list': '',
            'state': '',
            'rounds': random.randint(2,5),
            'tournament_date': '2013-07-01'
        }
    })

games = []
for game_id in range(game_count):
    p1 = random.choice(members)['pk']
    p2 = random.choice(filter(lambda m: m['pk'] != p1, members))['pk']
    date = dt.date.today() - dt.timedelta(days = random.randint(2,20))
    games.append({
        'pk': game_id,
        'model': 'agagd_core.game',
        'fields': {
            'pin_player_2': p2,
            'tournament_code': random.choice(tournaments)['pk'],
            'rated': '',
            'elab_date': date.strftime("%Y-%m-%d"),
            'handicap': random.randint(0, 2),
            'online': '',
            'color_2': '',
            'sgf_code': '',
            'komi': 0.0,
            'pin_player_1': p1,
            'rank_1': '',
            'result': '',
            'rank_2': '',
            'game_date': date.strftime("%Y-%m-%d"),
            'exclude': '',
            'round': '',
            'color_1': ''
        }
    })

chapters = [] 
for i, chap_code in enumerate(CHAPTER_CODES):
    chapters.append({
        'pk': i,
        'model': 'agagd_core.chapters',
        'fields': {
            'member_id': i,
            'code': chap_code,
            'name': random.choice(['Firefly Go Club', 'NBA Go Club', 'some other club']),
            'contact_text': random.choice(['Some contact info would go here.', '']),
            'contact': 'Some guy',
            'meeting_city': 'Seattle',
            'url': 'www.localhost-is-best-host.com',
        }
    }) 

print json.dumps(members + tournaments + games + chapters, indent=4)
