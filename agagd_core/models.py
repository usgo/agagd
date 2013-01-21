# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Authteam(models.Model):
    id = models.TextField(primary_key=True) # This field type is a guess.
    teamname = models.CharField(max_length=25)
    teamlead = models.CharField(max_length=25)
    status = models.CharField(max_length=10)
    class Meta:
        db_table = u'authteam'

class Authuser(models.Model):
    id = models.TextField(primary_key=True) # This field type is a guess.
    uname = models.CharField(max_length=25)
    passwd = models.CharField(max_length=32)
    team = models.CharField(max_length=25)
    level = models.TextField() # This field type is a guess.
    status = models.CharField(max_length=10)
    lastlogin = models.DateTimeField(null=True, blank=True)
    logincount = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = u'authuser'

class Changelog(models.Model):
    log_id = models.TextField(primary_key=True) # This field type is a guess.
    log_date = models.DateTimeField()
    model = models.CharField(max_length=255)
    record = models.CharField(max_length=255)
    record_id = models.CharField(max_length=255)
    user = models.CharField(max_length=255, blank=True)
    user_id = models.TextField(blank=True) # This field type is a guess.
    summary = models.CharField(max_length=255, blank=True)
    changes = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = u'changelog'

class Chapter(models.Model):
    chapter_code = models.CharField(max_length=4, primary_key=True, db_column=u'Chapter_Code') # x.
    chapter_descr = models.CharField(max_length=50, db_column=u'Chapter_Descr') # x.
    class Meta:
        db_table = u'chapter'

class Chapters(models.Model):
    member_id = models.TextField(primary_key=True) # This field type is a guess.
    name = models.CharField(max_length=255, blank=True)
    legacy_status = models.CharField(max_length=1, blank=True)
    code = models.CharField(max_length=4, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    rep_id = models.TextField(blank=True) # This field type is a guess.
    url = models.CharField(max_length=255, blank=True)
    meeting_city = models.CharField(max_length=255, blank=True)
    contact_html = models.TextField(blank=True)
    contact_text = models.TextField(blank=True)
    meeting_text = models.TextField(blank=True)
    size = models.CharField(max_length=255, blank=True)
    events = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    fees = models.CharField(max_length=255, blank=True)
    display = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'chapters'

class CommentsAuthors(models.Model):
    id = models.CharField(max_length=12, primary_key=True, db_column=u'Id') # x.
    last_name = models.CharField(max_length=50, db_column=u'Last_Name') # x.
    first_name = models.CharField(max_length=50, db_column=u'First_Name') # x.
    country = models.CharField(max_length=3, db_column=u'Country') # x.
    pin = models.TextField(db_column=u'PIN') # x. This field type is a guess.
    class Meta:
        db_table = u'comments_authors'

class Country(models.Model):
    country_code = models.CharField(max_length=2, primary_key=True, db_column=u'Country_Code') # x.
    country_descr = models.CharField(max_length=50, db_column=u'Country_Descr') # x.
    country_flag = models.CharField(max_length=4, db_column=u'Country_Flag', blank=True) # x.
    class Meta:
        db_table = u'country'

class Games(models.Model):
    game_id = models.IntegerField(primary_key=True, db_column=u'Game_ID') # x. This field type is a guess.
    tournament_code = models.CharField(max_length=20, db_column=u'Tournament_Code') # .
    game_date = models.DateField(db_column=u'Game_Date') # x.
    round = models.TextField(db_column=u'Round') # x. This field type is a guess.
    pin_player_1 = models.IntegerField(db_column=u'Pin_Player_1') # x. This field type is a guess.
    color_1 = models.CharField(max_length=1, db_column=u'Color_1') # x.
    rank_1 = models.CharField(max_length=3, db_column=u'Rank_1') # x.
    pin_player_2 = models.IntegerField(db_column=u'Pin_Player_2') # x. This field type is a guess.
    color_2 = models.CharField(max_length=1, db_column=u'Color_2') # x.
    rank_2 = models.CharField(max_length=3, db_column=u'Rank_2') # x.
    handicap = models.IntegerField(db_column=u'Handicap') # x. This field type is a guess.
    komi = models.FloatField(db_column=u'Komi') # x. This field type is a guess.
    result = models.CharField(max_length=1, db_column=u'Result') # x.
    sgf_code = models.CharField(max_length=26, db_column=u'Sgf_Code', blank=True) # x.
    online = models.TextField(db_column=u'Online', blank=True) # x. This field type is a guess.
    exclude = models.TextField(db_column=u'Exclude', blank=True) # x. This field type is a guess.
    rated = models.TextField(db_column=u'Rated', blank=True) # x. This field type is a guess.
    elab_date = models.DateField(db_column=u'Elab_Date') # x.
    class Meta:
        db_table = u'games'
        verbose_name = u'game'
        verbose_name_plural = u'games'

    def __unicode__(self):
        return u"Tournament %s Round %s, %s vs %s" % (self.tournament_code,
                self.round, self.pin_player_1, self.pin_player_2)

    def __str__(self):
        return str(self.__unicode__())

class Members(models.Model): 
    class Meta:
        db_table = u'members'
        verbose_name = u'member'
        verbose_name_plural = u'members'

    member_id = models.TextField(primary_key=True, editable=False) # This field type is a guess.
    legacy_updated = models.DateField(null=True, blank=True)
    legacy_web_updated = models.DateField(null=True, blank=True)
    legacy_new = models.TextField() # This field type is a guess.
    legacy_id = models.TextField(blank=True) # This field type is a guess.
    legacy_citizen_of = models.CharField(max_length=100, blank=True)
    legacy_source = models.CharField(max_length=5, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    given_names = models.CharField(max_length=255, blank=True)
    family_name = models.CharField(max_length=255, blank=True)
    renewal_due = models.DateField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    status = models.TextField(blank=True)
    type = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)
    cell = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    email2 = models.CharField(max_length=255, blank=True)
    chapter = models.CharField(max_length=100, blank=True)
    chapter_id = models.TextField(blank=True) # This field type is a guess.
    occupation = models.CharField(max_length=100, blank=True)
    citizen = models.TextField() # This field type is a guess.
    password_plaintext = models.CharField(max_length=255, blank=True, editable=False)
    secret_q = models.CharField(max_length=255, blank=True, editable=False)
    secret_a = models.CharField(max_length=255, blank=True, editable=False)
    last_login = models.DateTimeField(null=True, blank=True)
    reset_token = models.CharField(max_length=255, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    dues_last_paid = models.DateTimeField(null=True, blank=True)
    last_changed = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u"Player %s: %s %s (%s) " % (self.member_id, self.given_names,
                self.family_name, self.full_name)

class MembersPayments(models.Model):
    payment_id = models.TextField(primary_key=True) # This field type is a guess.
    member_id = models.TextField() # This field type is a guess.
    years = models.TextField(blank=True) # This field type is a guess.
    amount = models.TextField(blank=True) # This field type is a guess.
    legacy_payment_type = models.CharField(max_length=30, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    via = models.CharField(max_length=30, blank=True)
    processed_by = models.TextField(blank=True) # This field type is a guess.
    txn_id = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    promo = models.CharField(max_length=255, blank=True)
    payment_type = models.CharField(max_length=50, blank=True)
    legacy_payment_method = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'members_payments'

class MembersRegions(models.Model):
    region_id = models.TextField(primary_key=True) # This field type is a guess.
    region = models.CharField(max_length=255, blank=True)
    states = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'members_regions'

class Membership(models.Model):
    mtype = models.CharField(max_length=8, primary_key=True, db_column=u'MType') # x.
    membership_type = models.CharField(max_length=35, db_column=u'Membership_Type') # x.
    class Meta:
        db_table = u'membership'

