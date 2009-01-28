#-*- coding: utf-8 -*-
# Django settings for twa project.

from mysettings import *

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

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
ugettext = lambda s: s
LANGUAGES = (
        ('de', u'deutsch'),
        ('en', u'english'),
        ('ja', u'日本語'),
        )
LANGUAGE_CODE = 'de-de'

SEND_MAIL_ON_LOGIN = True
#SEND_MAIL_ON_LOGIN = False

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Alle URLs an SSL weiterleiten
SSL_URLS = [
    #r'.*',
    r'/admin/',
    r'/antrag/',
    r'/lang/',
    #r'/public/',
    r'/associations/',
    r'/association/',
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
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
 )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
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
    'twa.members',
    'twa.requests',
 )
