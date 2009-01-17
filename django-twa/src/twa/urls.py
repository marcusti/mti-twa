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
    ( r'^association/(\d+)/$', 'association' ),
    ( r'^dojos/$', 'dojos' ),
    ( r'^dojo/(\d+)/$', 'dojo' ),
    ( r'^dojos/csv/$', 'dojos_csv' ),
    ( r'^graduations/$', 'graduations' ),
    ( r'^info/$', 'info' ),
    ( r'^licenses/$', 'licenses' ),
    ( r'^license-requests/$', 'license_requests' ),
    ( r'^license-rejected/$', 'license_rejected' ),
    ( r'^licenses/xls/$', 'licenses_xls' ),
    ( r'^license-requests/xls/$', 'license_requests_xls' ),
    ( r'^login/$', 'twa_login' ),
    ( r'^logout/$', 'twa_logout' ),
    ( r'^members/$', 'members' ),
    ( r'^members2/$', 'members2' ),
    ( r'^member/(\d+)/$', 'member' ),
    ( r'^member-requests/$', 'member_requests' ),
    ( r'^member-requests/xls/$', 'membership_requests_xls' ),
    ( r'^members/csv/$', 'members_csv' ),
    ( r'^members/xls/$', 'members_xls' ),
    ( r'^nominations-xls$', 'nominations_xls' ),
#    ( r'^rosetta/', include('rosetta.urls') ),
    ( r'^suggestions/$', 'suggestions' ),
 )
