# A simple script to generate fake data
import sys, random, json

USAGE = 'Usage: python make_fake_fixtures.py [num_of_members] [num_of_games]'
GIVEN_NAMES = [ 'bruce', 'malcolm', 'kobe', 'peter', 'kaylee', 'inara', ]
LAST_NAMES = [ 'lee', 'reynolds', 'bryant', 'parker', 'frye', 'serra', ]

if len(sys.argv) != 3:
    print USAGE
    quit()

try:
    MEMBER_COUNT = int(sys.argv[1])
    GAME_COUNT = int(sys.argv[1])
except ValueError:
    print USAGE
    quit()

members = []
for member_id in range(MEMBER_COUNT):
    first_name = random.choice(GIVEN_NAMES)
    last_name = random.choice(LAST_NAMES)
    members.append({
        'pk': str(member_id),
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
            'country': 'some country',
            'chapter': 'some chapter',
            'chapter_id': 'MAYBE_FK',
            'occupation': '',
            'citizen': 'yes',
            'password': 'hallo!',
            'last_changed': None
        }
    })

games = []
for game_id in range(GAME_COUNT):
    games.append({
        'pk': str(game_id),
        'model': 'agagd_core.game',
        'fields': {
            'game_id': game_id,
        }
    })

print json.dumps(members, indent=4)
