from agagd_core.models import Chapter, Chapters, Country, Game, Member, MembersRegions, Membership
from django.contrib import admin

class MemberAdmin(admin.ModelAdmin): 
    list_display = ('member_id', 'full_name', 'join_date', 'chapter', 'chapter_id')

admin.site.register(Chapter)
admin.site.register(Chapters)
admin.site.register(Country)
admin.site.register(Game)
admin.site.register(Member, MemberAdmin)
admin.site.register(Membership)
admin.site.register(MembersRegions)
