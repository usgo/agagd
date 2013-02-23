from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin 
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agagd.views.home', name='home'),
    # url(r'^agagd/', include('agagd.foo.urls')),
    #url(r'^gd/', include('agagd_core.urls')),

     (r'^$', 'agagd_core.views.index'),
     (r'.php$', 'agagd_core.views.index'),
     (r'^member_fetch/$', 'agagd_core.views.member_fetch'),
     (r'^member_search_form/$', 'agagd_core.views.member_search_form'),

     (r'^player/(?P<member_id>\d+)/$', 'agagd_core.views.member_detail'),
     (r'^player/(?P<member_id>\d+)/vs/(?P<other_id>\d+)$', 'agagd_core.views.member_vs'), 
     (r'^ratings/(?P<member_id>\d+)/$', 'agagd_core.views.member_ratings'), 

     (r'^tournaments/$', 'agagd_core.views.tournament_list'),
     (r'^tournaments/(?P<tourn_code>\w{1,20})/$', 'agagd_core.views.tournament_detail'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
from django.conf import settings
if settings.ADMIN_ENABLED:
    urlpatterns += patterns(
        url(r'^admin/', include(admin.site.urls)),
        )

