from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns( '',
    # Admin
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),
    ( r'^admin/(.*)', admin.site.root ),
    ( r'^i18n/', include( 'django.conf.urls.i18n' ) ),
    #( r'^logout/$', 'django.contrib.auth.views.logout_then_login' ),
    #( r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'} ),
 )

if settings.DEBUG:
    urlpatterns += patterns( '',
        ( r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),
     )

urlpatterns += patterns( 'twa.members.views',
    ( r'^$', 'index' ),
    ( r'^lang/(.*)/$', 'set_lang' ),
    ( r'^public/$', 'public' ),
    ( r'^associations/$', 'associations' ),
    ( r'^associations2/$', 'associations2' ),
    ( r'^association/(\d+)/$', 'association' ),
    ( r'^dojos/$', 'dojos' ),
    ( r'^dojos2/$', 'dojos2' ),
    ( r'^dojo/(\d+)/$', 'dojo' ),
    ( r'^dojo2/(\d+)/$', 'dojo2' ),
    ( r'^dojos/csv/$', 'dojos_csv' ),
    ( r'^graduations/$', 'graduations' ),
    ( r'^graduations2/$', 'graduations2' ),
    ( r'^info/$', 'info' ),
    ( r'^licenses/$', 'licenses' ),
    ( r'^licenses2/$', 'licenses2' ),
    ( r'^license-requests/$', 'license_requests' ),
    ( r'^license-requests2/$', 'license_requests2' ),
    ( r'^license-rejected/$', 'license_rejected' ),
    ( r'^licenses/xls/$', 'licenses_xls' ),
    ( r'^license-requests/xls/$', 'license_requests_xls' ),
    ( r'^login/$', 'twa_login' ),
    ( r'^login2/$', 'twa_login2' ),
    ( r'^logout/$', 'twa_logout' ),
    ( r'^logout2/$', 'twa_logout2' ),
    ( r'^members/$', 'members' ),
    ( r'^member2/(\d+)/$', 'member2' ),
    ( r'^members2/$', 'members2' ),
    ( r'^members2/all/$', 'members_all' ),
    ( r'^member/(\d+)/$', 'member' ),
    ( r'^member-requests/$', 'member_requests' ),
    ( r'^member-requests2/$', 'member_requests2' ),
    ( r'^member-requests/xls/$', 'membership_requests_xls' ),
    ( r'^members/csv/$', 'members_csv' ),
    ( r'^members/xls/$', 'members_xls' ),
    ( r'^nominations-xls$', 'nominations_xls' ),
#    ( r'^rosetta/', include('rosetta.urls') ),
    ( r'^suggestions/$', 'suggestions' ),
    ( r'^suggestions2/$', 'suggestions2' ),
 )
