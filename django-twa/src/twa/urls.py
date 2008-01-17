from django.conf.urls.defaults import *

urlpatterns = patterns( '',
    # Admin
    ( r'^admin/', include( 'django.contrib.admin.urls' ) ),
    ( r'^i18n/', include( 'django.conf.urls.i18n' ) ),
    ( r'^accounts/login/$', 'django.contrib.auth.views.login' ),
    ( r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'} ),
    ( r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/max/eclipse/workspace/django-twa/htdocs/static'} ),

 )
urlpatterns += patterns( 'django.views.generic.simple',
 )

urlpatterns += patterns( 'twa.members.views',
    ( r'^$', 'index' ),
    ( r'^dojos/', 'dojos' ),
    ( r'^dojo/(\d+)/', 'dojo' ),
    ( r'^members/', 'members' ),
    ( r'^csv/', 'dojos_csv' ),
 )
