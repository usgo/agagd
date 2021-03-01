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
    member_id = models.AutoField(primary_key=True)
    legacy_id = models.IntegerField(max_length=11, blank=True)
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
    chapter_id = models.IntegerField(max_length=11, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    citizen = models.SmallIntegerField(max_length=6)
    password = models.CharField(max_length=255, blank=True)
    last_changed = models.DateTimeField(null=True, blank=True)
    renewal_due = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{0} ({1})".format(self.full_name, self.member_id)

    class Meta:
        db_table = 'members'
        verbose_name = 'member'
        verbose_name_plural = 'members'
        managed = False

class Chapters(models.Model):
    # The member_id for a chapter is the same in this table and in the chapter's corresponding Member object.
    member_id = models.ForeignKey(
            Member,
            db_column='member_id',
            primary_key=True,
            on_delete=models.DO_NOTHING
    )

    name = models.CharField(max_length=255, blank=True)
    legacy_status = models.CharField(max_length=1, blank=True)
    # code is the 4-letter chapter code, which is now deprecated. It will remain
    # in place so that we can redirect URLs using the chapter code to the appropriate member_id-based link.
    code = models.CharField(max_length=4, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    rep_id = models.IntegerField(blank=True)
    url = models.CharField(max_length=255, blank=True)
    meeting_city = models.CharField(max_length=255, blank=True)
    contact_html = models.TextField(blank=True)
    contact_text = models.TextField(blank=True)
    meeting_text = models.TextField(blank=True)
    size = models.CharField(max_length=255, blank=True)
    events = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    fees = models.CharField(max_length=255, blank=True)
    display = models.SmallIntegerField(max_length=1)

    class Meta:
        managed = False
        db_table = 'chapters'

class Country(models.Model):
    country_code = models.CharField(max_length=2, primary_key=True, db_column='Country_Code')
    country_descr = models.CharField(max_length=50, db_column='Country_Descr')
    country_flag = models.CharField(max_length=4, db_column='Country_Flag', blank=True)

    class Meta:
        managed = False
        db_table = 'country'

class Tournament(models.Model):
    tournament_code = models.CharField(max_length=20, primary_key=True, db_column='Tournament_Code')
    description = models.CharField(max_length=80, db_column='Tournament_Descr')
    tournament_date = models.DateField(db_column='Tournament_Date')
    elab_date = models.DateField(db_column='Elab_Date')
    city = models.CharField(max_length=30, db_column='City')
    state = models.CharField(max_length=2, db_column='State_Code', blank=True)
    rounds = models.SmallIntegerField(max_length=2, db_column='Rounds')
    total_players = models.SmallIntegerField(max_length=3, db_column='Total_Players')
    wall_list = models.TextField(db_column='Wallist')

    def __str__(self):
        return "{0} - on {1} with {2} players".format(self.tournament_code, self.tournament_date, self.total_players)

    def __unicode__(self):
        if self.description:
            if len(self.description) > 40:
                return "{0}...".format(self.description[0:37])
            return "{0}".format(self.description)
        return "{0}".format(self.pk)
    
    class Meta:
        managed = False
        db_table= 'tournaments'
        verbose_name = 'tournament'
        verbose_name_plural = 'tournaments'

class TopDan(models.Model):
    member_id = models.IntegerField(primary_key=True, db_column='member_id')
    full_name = models.CharField(max_length=255, db_column='full_name')
    rating = models.CharField(max_length=42, db_column='rating')

    class Meta:
        managed = False
        db_table = 'top_dan_view'
        verbose_name = 'top_dan_view'
        verbose_name_plural = 'top_dan_view'

class TopKyu(models.Model):
    member_id = models.IntegerField(primary_key=True, db_column='member_id')
    full_name = models.CharField(max_length=255, db_column='full_name')
    rating = models.CharField(max_length=42, db_column='rating')

    class Meta:
        managed = False
        db_table = 'top_kyu_view'
        verbose_name = 'top_kyu_view'
        verbose_name_plural = 'top_kyu_view'

class MostRatedGamesPastYear(models.Model):
    member_id = models.IntegerField(primary_key=True, db_column='pin')
    name = models.CharField(max_length=65, db_column='Name')
    total = models.BigIntegerField(db_column='Game_Count')

    class Meta:
        managed = False
        db_table = 'most_rated_games_view'
        verbose_name = 'most_rated_games_view'
        verbose_name_plural = 'most_rated_games_view'

class MostTournamentsPastYear(models.Model):
    member_id = models.IntegerField(primary_key=True, db_column='pin')
    name = models.CharField(max_length=65, db_column='Name')
    total = models.BigIntegerField(db_column='Tournament_Count')

    class Meta:
        managed = False
        db_table = 'most_tournaments_view'
        verbose_name = 'most_tournaments_view'
        verbose_name_plural = 'most_tournaments_view'

class Game(models.Model):
    game_id = models.IntegerField(max_length=10, primary_key=True, db_column='Game_ID')
    game_date = models.DateField(db_column='Game_Date')
    round = models.SmallIntegerField(max_length=2, db_column='Round')
    color_1 = models.CharField(max_length=1, db_column='Color_1')
    rank_1 = models.CharField(max_length=3, db_column='Rank_1')
    color_2 = models.CharField(max_length=1, db_column='Color_2')
    rank_2 = models.CharField(max_length=3, db_column='Rank_2')
    handicap = models.SmallIntegerField(max_length=2, db_column='Handicap')
    komi = models.SmallIntegerField(max_length=2, db_column='Komi')
    result = models.CharField(max_length=1, db_column='Result')
    sgf_code = models.CharField(max_length=26, db_column='Sgf_Code', blank=True)
    online = models.SmallIntegerField(max_length=1, db_column='Online', blank=True)
    exclude = models.SmallIntegerField(max_length=1, db_column='Exclude', blank=True)
    rated = models.SmallIntegerField(max_length=1, db_column='Rated', blank=True)
    elab_date = models.DateField(db_column='Elab_Date')

    tournament_code = models.ForeignKey(
            Tournament,
            related_name='games_in_tourney',
            db_column='Tournament_Code',
            on_delete=models.DO_NOTHING
    )

    pin_player_1 = models.ForeignKey(
            Member,
            db_column='Pin_Player_1',
            related_name='games_as_p1',
            on_delete=models.DO_NOTHING
    )

    pin_player_2 = models.ForeignKey(
            Member,
            db_column='Pin_Player_2',
            related_name='games_as_p2',
            on_delete=models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = 'games'
        verbose_name = 'game'
        verbose_name_plural = 'games'

    def __str__(self):
        return "Tournament {0} Round {1}, {2} vs {3}".format(
            self.tournament_code,
            self.round,
            self.pin_player_1,
            self.pin_player_2
        )

    # player_other_than(self, one_player)
    #
    # returns the player opposite whichever player
    # is provided to player_other_than
    def player_other_than(self, one_player):
        if (one_player == self.pin_player_1):
            return self.pin_player_2
        return self.pin_player_1

    def winner(self):
        if self.result == self.color_1:
            return self.pin_player_1
        if self.result == self.color_2:
            return self.pin_player_2
        raise ValueError

    def won_by(self, p1):
        return self.winner() == p1

# Updated Rating Information Table for Players.
class Players(models.Model):
    pin_player = models.ForeignKey(
            Member,
            db_column='Pin_Player',
            primary_key=True,
            on_delete=models.DO_NOTHING
    )
    
    # Member Name Fields
    # Note: These are just for completeness. They should be removed when 
    #       the mysql views are migrated into ORM within the AGAGD app. 
    #       Views include: most_rated_games_view, most_tournaments_view,
    #                      most_tournaments_view and top_kyu_view.
    name = models.CharField(max_length=30, db_column='Name')
    last_name = models.CharField(max_length=30, db_column='Last_Name')
    
    rating = models.FloatField(db_column='Rating')
    sigma = models.FloatField(db_column='Sigma')
    elab_date = models.DateField(db_column='Elab_Date')

    class Meta:
        managed = False
        db_table = 'players'

class Rating(models.Model):
    # ForeignKey for the Members
    pin_player = models.ForeignKey(
            Member,
            db_column='Pin_Player',
            related_name='ratings_set',
            on_delete=models.DO_NOTHING
    )

    tournament = models.ForeignKey(
            Tournament,
            db_column='Tournament_Code',
            related_name='ratings_set',
            on_delete=models.DO_NOTHING
    )

    rating = models.FloatField(db_column='Rating') # x. This field type is a guess.
    sigma = models.FloatField(db_column='Sigma') # x. This field type is a guess.
    elab_date = models.DateField(db_column='Elab_Date')

    class Meta:
        managed = False
        db_table = 'ratings'

class MembersRegions(models.Model):
    region_id = models.IntegerField(max_length=11, primary_key=True)
    region = models.CharField(max_length=255, blank=True)
    states = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'members_regions'

class Membership(models.Model):
    mtype = models.CharField(max_length=8, primary_key=True, db_column='MType')
    membership_type = models.CharField(max_length=35, db_column='Membership_Type')

    class Meta:
        managed = False
        db_table = 'membership'
