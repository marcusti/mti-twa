from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from twa.members.models import NewsFeed

admin.autodiscover()

urlpatterns = patterns( '',
    # Admin
    ( r'^admin/doc/', include( 'django.contrib.admindocs.urls' ) ),
    #( r'^admin/(.*)', admin.site.root ),
    ( r'^admin/', include(admin.site.urls) ),
    ( r'^i18n/', include( 'django.conf.urls.i18n' ) ),
    #( r'^logout/$', 'django.contrib.auth.views.logout_then_login' ),
    #( r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'} ),
 )

if settings.DEBUG:
    urlpatterns += patterns( '',
        ( r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT} ),
     )

newsfeed = {
    'news-de': NewsFeed,
    'news-en': NewsFeed,
}

urlpatterns += patterns( '',
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': newsfeed}),
)

urlpatterns += patterns( 'twa.members.views',
#    ( r'^$', 'index' ),
    ( r'^lang/(.*)/$', 'set_lang' ),
    ( r'^$', 'public' ),
    ( r'^antrag/$', 'antrag' ),
    ( r'^antrag/$', 'membership_online_request' ),
    ( r'^associations/$', 'associations' ),
    ( r'^association/(\d+)/$', 'association' ),
    ( r'^document/(.*)/$', 'documents_handler' ),
    ( r'^image/(.*)/(.*)/$', 'image_handler' ),
    ( r'^dojos/$', 'dojos2' ),
    ( r'^dojo/(\d+)/$', 'dojo2' ),
    ( r'^dojo/(\d+)/csv/$', 'dojo_csv' ),
    ( r'^dojos/csv/$', 'dojos_csv' ),
    ( r'^downloads/$', 'downloads' ),
    ( r'^graduations/$', 'graduations2' ),
    ( r'^info/$', 'info' ),
    ( r'^licensees/$', 'licensees' ),
    ( r'^licenses/$', 'licenses' ),
    ( r'^licenses/dojo/(?P<dojo_id>\d+)/$', 'licenses' ),
    ( r'^licenses/twa/$', 'licenses', {'twa_status': True} ),
    ( r'^licenses/notwa/$', 'licenses', {'twa_status': False} ),
    ( r'^license-requests/$', 'license_requests' ),
    ( r'^license-rejected/$', 'license_rejected' ),
    ( r'^licenses/xls/$', 'licenses_xls' ),
    ( r'^license-requests/xls/$', 'license_requests_xls' ),
    ( r'^login/$', 'twa_login' ),
    ( r'^logout/$', 'twa_logout' ),
    ( r'^members/$', 'members2' ),
    ( r'^members/all/$', 'members_all' ),
    ( r'^member/(\d+)/$', 'member2' ),
    ( r'^member-requests/$', 'member_requests' ),
    ( r'^member-requests/dojo/(?P<dojo_id>\d+)/$', 'member_requests' ),
    ( r'^member-requests/region/(?P<region_id>\d+)/$', 'member_requests' ),
    ( r'^member-requests/open/$', 'member_requests', {'status': '1'} ),
    ( r'^member-requests/accepted/$', 'member_requests', {'status': '2'} ),
    ( r'^member-requests/to-be-confirmed/$', 'member_requests', {'status': '6'} ),
    ( r'^member-requests/confirmed/$', 'member_requests', {'status': '5'} ),
    ( r'^member-requests/verify/$', 'member_requests', {'status': '4'} ),
    ( r'^member-requests/member/$', 'member_requests', {'status': '10'} ),
    ( r'^member-requests/nopayment/$', 'member_requests', {'no_payment_filter': True} ),
    ( r'^member-requests/confirmation-email/$', 'confirmation_email' ),
    ( r'^member-requests/accept_open_requests/$', 'accept_open_requests' ),
    ( r'^member-requests/twa-ids/$', 'create_twa_ids' ),
    ( r'^member-requests/xls/$', 'membership_requests_xls' ),
    ( r'^members/csv/$', 'members_csv' ),
    ( r'^members/xls/$', 'members_xls' ),
    ( r'^news/$', 'news_archive' ),
    ( r'^news/(\d+)/$', 'news' ),
    ( r'^news/preview/(\d+)/$', 'news_preview' ),
    ( r'^nominations-xls$', 'nominations_xls' ),
    ( r'^suggestions/$', 'suggestions2' ),
    ( r'^twa-region/$', 'twa_region' ),
    ( r'^twa-region/region/(?P<region_id>\d+)/$', 'twa_region' ),
 )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )