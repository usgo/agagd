# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Member(models.Model):
    class Meta:
        db_table = u'members'
        verbose_name = u'member'
        verbose_name_plural = u'members'
        managed = False

    member_id = models.AutoField(primary_key=True)
    legacy_id = models.TextField(blank=True) # This field type is a guess.
    full_name = models.CharField(max_length=255, blank=True, db_index=True)
    given_names = models.CharField(max_length=255, blank=True)
    family_name = models.CharField(max_length=255, blank=True, db_index=True)
    join_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255)
    chapter = models.CharField(max_length=100, blank=True)
    chapter_id = models.TextField(blank=True) # This field type is a guess.
    occupation = models.CharField(max_length=100, blank=True)
    citizen = models.TextField() # This field type is a guess.
    password = models.CharField(max_length=255, blank=True)
    last_changed = models.DateTimeField(null=True, blank=True)
    renewal_due = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    def __unicode__(self):
        return u" %s (%s) " % (self.full_name, self.member_id, )

class Chapter(models.Model):
    chapter_code = models.CharField(max_length=4, primary_key=True, db_column=u'Chapter_Code') # x.
    chapter_descr = models.CharField(max_length=50, db_column=u'Chapter_Descr') # x.
    class Meta:
        db_table = u'chapter'
        managed = False

class Chapters(models.Model):
    # ForeignKey for Member
    member = models.ForeignKey(Member)

    # TODO this is not member_id? seems more like a normal pk for ChapterInfo
    member_id = models.CharField(max_length=255, primary_key=True) # This field type is a guess.
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
        managed = False
        db_table = u'chapters'

class CommentsAuthors(models.Model):
    id = models.CharField(max_length=12, primary_key=True, db_column=u'Id') # x.
    last_name = models.CharField(max_length=50, db_column=u'Last_Name') # x.
    first_name = models.CharField(max_length=50, db_column=u'First_Name') # x.
    country = models.CharField(max_length=3, db_column=u'Country') # x.
    pin = models.TextField(db_column=u'PIN') # x. This field type is a guess.
    class Meta:
        managed = False
        db_table = u'comments_authors'

class Country(models.Model):
    country_code = models.CharField(max_length=2, primary_key=True, db_column=u'Country_Code') # x.
    country_descr = models.CharField(max_length=50, db_column=u'Country_Descr') # x.
    country_flag = models.CharField(max_length=4, db_column=u'Country_Flag', blank=True) # x.
    class Meta:
        managed = False
        db_table = u'country'

class Tournament(models.Model):
    tournament_code = models.CharField(max_length=20, primary_key=True, db_column=u'Tournament_Code')
    description = models.TextField(db_column='Tournament_Descr')
    tournament_date = models.DateField(db_column=u'Tournament_Date')
    elab_date = models.DateField(db_column=u'Elab_Date')
    city = models.CharField(max_length=30, db_column=u'City')
    state = models.CharField(max_length=2, db_column=u'State_Code', blank=True)
    rounds = models.IntegerField(db_column='Rounds')
    total_players = models.IntegerField(db_column='Total_Players')
    wall_list = models.TextField(db_column='Wallist')
    def __str__(self):
        return "%s - on %s with %d players" % (self.tournament_code, self.tournament_date, self.total_players)
    def __unicode__(self):
        if self.description:
            if len(self.description) > 40:
                return u'%s...' % self.description[0:37]
            return u'%s' % self.description
        else:
            return u'%s' % self.pk
    
    class Meta:
        managed = False
        db_table= u'tournaments'
        verbose_name = u'tournament'
        verbose_name_plural = u'tournaments'

class TopDan(models.Model):
    member_id = models.IntegerField(primary_key=True, db_column=u'member_id')
    full_name = models.CharField(max_length=255, db_column=u'full_name')
    rating = models.CharField(max_length=42, db_column=u'rating')

    class Meta:
        managed = False
        db_table = u'top_dan_view'
        verbose_name = u'top_dan_view'
        verbose_name_plural = u'top_dan_view'

class TopKyu(models.Model):
    member_id = models.IntegerField(primary_key=True, db_column=u'member_id')
    full_name = models.CharField(max_length=255, db_column=u'full_name')
    rating = models.CharField(max_length=42, db_column=u'rating')

    class Meta:
        managed = False
        db_table = u'top_kyu_view'
        verbose_name = u'top_kyu_view'
        verbose_name_plural = u'top_kyu_view'

class MostRatedGamesPastYear(models.Model):
    pin = models.IntegerField(primary_key=True, db_column=u'pin')
    name = models.CharField(max_length=65, db_column=u'Name')
    total = models.BigIntegerField(db_column=u'Game_Count')

    class Meta:
        managed = False
        db_table = u'most_rated_games_view'
        verbose_name = u'most_rated_games_view'
        verbose_name_plural = u'most_rated_games_view'

class MostTournamentsPastYear(models.Model):
    pin = models.IntegerField(primary_key=True, db_column=u'pin')
    name = models.CharField(max_length=65, db_column=u'Name')
    total = models.BigIntegerField(db_column=u'Tournament_Count')

    class Meta:
        managed = False
        db_table = u'most_tournaments_view'
        verbose_name = u'most_tournaments_view'
        verbose_name_plural = u'most_tournaments_view'

class Game(models.Model):
    game_id = models.AutoField(primary_key=True, db_column=u'Game_ID') # x. This field type is a guess.
    game_date = models.DateField(db_column=u'Game_Date') # x.
    round = models.TextField(db_column=u'Round') # x. This field type is a guess.
    color_1 = models.CharField(max_length=1, db_column=u'Color_1') # x.
    rank_1 = models.CharField(max_length=3, db_column=u'Rank_1') # x.
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

    tournament_code = models.ForeignKey(Tournament, related_name='games_in_tourney', db_column=u'Tournament_Code') # .
    pin_player_1 = models.ForeignKey(Member, db_column=u'Pin_Player_1', related_name='games_as_p1')
    pin_player_2 = models.ForeignKey(Member, db_column=u'Pin_Player_2', related_name='games_as_p2')

    class Meta:
        managed = False
        db_table = u'games'
        verbose_name = u'game'
        verbose_name_plural = u'games'

    def __unicode__(self):
        return u"Tournament %s Round %s, %s vs %s" % (self.tournament_code,
                self.round, self.pin_player_1, self.pin_player_2)

    def __str__(self):
        return str(self.__unicode__())

    def player_other_than(self, one_player):
        """ returns the member of the other player. """
        return self.pin_player_2 if (one_player == self.pin_player_1) else self.pin_player_1

    def winner(self):
        if self.result == self.color_1:
            return self.pin_player_1
        if self.result == self.color_2:
            return self.pin_player_2
        raise ValueError

    def won_by(self, p1):
        return self.winner() == p1

class Rating(models.Model):
    # ForeignKey for the Members
    member_id = models.ForeignKey(Member, db_column=u'Pin_Player')
    pin_player = models.ForeignKey(Member, db_column=u'Pin_Player', related_name='ratings_set', primary_key=True)
    tournament = models.ForeignKey(Tournament, db_column=u'Tournament_Code', related_name='ratings_set')
    rating = models.FloatField(db_column=u'Rating') # x. This field type is a guess.
    sigma = models.FloatField(db_column=u'Sigma') # x. This field type is a guess.
    elab_date = models.DateField(db_column=u'Elab_Date')
    class Meta:
        managed = False
        db_table = u'ratings'

class MembersRegions(models.Model):
    region_id = models.CharField(max_length=255, primary_key=True) # This field type is a guess.
    region = models.CharField(max_length=255, blank=True)
    states = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = u'members_regions'

class Membership(models.Model):
    mtype = models.CharField(max_length=8, primary_key=True, db_column=u'MType') # x.
    membership_type = models.CharField(max_length=35, db_column=u'Membership_Type') # x.
    class Meta:
        managed = False
        db_table = u'membership'
