import sys

USAGE = 'Usage: python make_fake_fixtures.py [num_of_members]'
GIVEN_NAMES = [ 'bruce', 'malcolm', 'kobe', 'peter', 'kaylee', 'inara', ]
LAST_NAMES = [ 'lee', 'reynolds', 'bryant', 'parker', 'frye', 'serra', ]

if len(sys.argv) != 2:
    print USAGE
    quit()

try:
    MEMBER_COUNT = int(sys.argv[1])
except ValueError:
    print USAGE
    quit()

members = []
for member_id in range(MEMBER_COUNT):
    members.append({
        'pk': str(member_id),
        'model': 'agagd_core.members',
        'fields': {
            'member_id': '1',
            'legacy_id': '',
            'full_name': 'bruce lee',
            'given_names': 'bruce',
            'family_name': 'lee',
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
