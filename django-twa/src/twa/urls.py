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
#    ( r'^$', 'index' ),
    ( r'^lang/(.*)/$', 'set_lang' ),
    ( r'^$', 'public' ),
    ( r'^antrag/$', 'antrag' ),
    ( r'^antrag/$', 'membership_online_request' ),
    ( r'^associations/$', 'associations' ),
    ( r'^association/(\d+)/$', 'association' ),
    ( r'^dojos/$', 'dojos2' ),
    ( r'^dojo/(\d+)/$', 'dojo2' ),
    ( r'^dojos/csv/$', 'dojos_csv' ),
    ( r'^downloads/$', 'downloads' ),
    ( r'^graduations/$', 'graduations2' ),
    ( r'^info/$', 'info' ),
    ( r'^licenses/$', 'licenses2' ),
    ( r'^license-requests/$', 'license_requests2' ),
    ( r'^license-rejected/$', 'license_rejected' ),
    ( r'^licenses/xls/$', 'licenses_xls' ),
    ( r'^license-requests/xls/$', 'license_requests_xls' ),
    ( r'^login/$', 'twa_login' ),
    ( r'^logout/$', 'twa_logout' ),
    ( r'^members/$', 'members2' ),
    ( r'^members/all/$', 'members_all' ),
    ( r'^member/(\d+)/$', 'member2' ),
    ( r'^member-requests/$', 'member_requests2' ),
    ( r'^member-requests/xls/$', 'membership_requests_xls' ),
    ( r'^members/csv/$', 'members_csv' ),
    ( r'^members/xls/$', 'members_xls' ),
    ( r'^news/$', 'news_archive' ),
    ( r'^news/(\d+)/$', 'news' ),
    ( r'^news/preview/(\d+)/$', 'news_preview' ),
    ( r'^nominations-xls$', 'nominations_xls' ),
    ( r'^suggestions/$', 'suggestions2' ),
 )
