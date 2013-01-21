
from agagd_core.models import Authteam, Authuser, Changelog, Chapter, Chapters, CommentsAuthors, Country, Games, Members, MembersRegions, Membership  
from django.contrib import admin

class MemberAdmin(admin.ModelAdmin): 
    list_display = ('member_id', 'full_name', 'join_date', 'chapter', 'chapter_id')

admin.site.register(Authteam)
admin.site.register(Authuser)
admin.site.register(Changelog)
admin.site.register(Chapter)
admin.site.register(Chapters)
admin.site.register(CommentsAuthors)
admin.site.register(Country)
admin.site.register(Games)
admin.site.register(Members, MemberAdmin)
admin.site.register(Membership)
admin.site.register(MembersRegions)
