#-*- coding: utf-8 -*-
# Django settings for twa project.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
ugettext = lambda s: s
LANGUAGES = (
        ('de', u'deutsch'),
        ('en', u'english'),
        ('ja', u'日本語'),
        )
LANGUAGE_CODE = 'de'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TMP_DIR = '/tmp/'

# Diese URLs an SSL weiterleiten
SSL_URLS = [
    #r'.*',
    r'/admin/',
    #r'/antrag/',
    #r'/lang/',
    #r'/public/',
    r'/associations/',
    r'/association/',
    r'/document/',
    r'/image/',
    r'/dojos/',
    r'/dojo/',
    r'/graduations/',
    r'/info/',
    r'/licenses/',
    r'/license-requests/',
    r'/license-rejected/',
    r'/login/',
    r'/logout/',
    r'/members/',
    r'/member/',
    r'/member-requests/',
    r'/nominations-xls',
    r'/suggestions/',
    r'/rosetta/',
    r'/translate/',
    r'/twa-region/',
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'twa.members.ssl.SSLRedirect',
 )

ROOT_URLCONF = 'twa.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',

    # 'rosetta',    # translating applications
    'south',      # db migrations

    'debug_toolbar',
    'twa.members',
    # 'twa.requests',
 )

try:
    from mysettings import *
except ImportError:
    pass
