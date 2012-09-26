from os.path import realpath, dirname, join
import os
#,import re

from hsdjango import settings_utils 
from hsdjango.settings_base2 import *
from hapicrank import task_queues as tq
from sanetime import delta

# Django settings for webinar project.

#ADMINS = (
    ## ('Your Name', 'your_email@example.com'),
#)

#MANAGERS = ADMINS

#LOG_PATH = "/tmp/hubspot/logs"

# local-specific db's
DATABASES = {
    'default': { 
        'HOST': 'localhost',
        'NAME': 'webinars',
        'USER': 'webinars',
        'PASSWORD': '__SECRET__',
        'ENGINE': 'django.db.backends.mysql',
    },

    'segments': {
        'HOST': 'EXAMPLE_DB_HOST',
        'NAME': 'SearchService',
        'USER': 'SUSR_Webinars',
        'PASSWORD': '__SECRET__',
        'ENGINE': 'django.db.backends.mysql'
    },

    'sfdc_info': {
        'HOST': 'EXAMPLE_DB_HOST',
        'NAME': 'sfdc',
        'USER': 'app_webinars',
        'PASSWORD': '__SECRET__',
        'ENGINE': 'django.db.backends.mysql'
    }
}

DATABASE_ROUTERS = ['segments.routers.SegmentsRouter', 'sfdc_info.routers.SfdcInfoRouter']

SENTRY_DSN = 'https://TOKEN:PASSWORD@app.getsentry.com/01122357'
SENTRY_ENABLED = True


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/New_York'
TIME_ZONE = 'UTC' # important since our app is assuming all dt's coming out of datetime fields for instance are in UTC

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''


# Make this unique, and don't share it with anybody.
SECRET_KEY = '#p7aos11xxx2dr8syj=c)hf!@#%973&_*&vxa1&9l3hbca2%hk(lgl!pwr'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

INTERNAL_IPS = ('127.0.0.1','localhost')

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
#    'hsdjango.middleware.SpacelessMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'hubspot_marketplacex.django.middleware.MockCanvasMiddleware',

# order very important here
    'marketplace.MockMiddleware',
    'marketplace.ErrorGogglesMiddleware',
    'marketplace.AuthMiddleware',
    'marketplace.AnchorFixMiddleware',
    'marketplace.DebugModeLoggingMiddleware',
#    'hsdjango.middleware.MarketplaceMiddleware',
#    'hsdjango.middleware.HubSpotMiddleware',
)


ROOT_URLCONF = 'webinars_web.urls'

PROJ_DIR =dirname(realpath(__file__))
TEMPLATE_DIRS = (
    join(PROJ_DIR, "webinars/templates"),
    
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'hsdjango',
    'hsforms',
    'segments',
    'sfdc_info',
    'webinars_web.webinars',
    'south',
#    'floppyforms',
#    'uni_form',
    'style_guide',
    'debug_toolbar',
    'gunicorn',
)

if os.environ.get('LOCAL_DEV'): 
    INSTALLED_APPS += ('debug_toolbar','gunicorn', 'template_repl')
    try:
        index = MIDDLEWARE_CLASSES.index('django.middleware.common.CommonMiddleware')
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES[0:index] + ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES[index:]
    except ValueError:
        pass


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOGGING = {
    #'version': 1,
    #'disable_existing_loggers': False,
    #'formatters': {
		#'detailed': {
            #'format': '%(asctime)s %(module)-17s line:%(lineno)-4d ' '%(levelname)-8s %(message)s', } },
    #'handlers': {
        #'null': {
            #'level': 'DEBUG',
            #'class': 'django.utils.log.NullHandler' },
        #'mail_admins': {
            #'level': 'ERROR',
            #'class': 'django.utils.log.AdminEmailHandler' },
        #'console': {
            #'level': 'DEBUG',
            #'class': 'logging.StreamHandler',
			#'formatter': 'detailed',
            #'stream': 'ext://sys.stdout' } },
    #'loggers': {
        #'django.request': {
            #'handlers': ['mail_admins'],
            #'level': 'ERROR',
            #'propagate': True, },
        #'django.db': {
            #'handlers': ['null'],
            #'level': 'DEBUG',
            #'propogate': True, },
        #'sync': {
            #'handlers': ['console'],
            #'level': 'DEBUG',
            #'propagate': True, } } }

# Don't forget to define an app-specific context processor
# which bundles all the static files you want included
# and defines which screen id you're working with.
# In your app's settings.py file, include this file and
# append your processor to the list.
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.contrib.messages.context_processors.messages",
    "hsdjango.context_processors.static_processor",
#    "hsdjango.context_processors.portal_processor",
    "hsdjango.context_processors.hs_processor",
    "webinars_web.context_processors.webinars_processor",
)

HUBSPOT_API_KEY = '__SECRET__API__KEY'
GTW_API_KEY = '__SECRET__GTW__API__KEY'

DEBUG = True
TEMPLATE_DEBUG = True

LOGGING = settings_utils.logging('webinars_web',True)

LOGGING['loggers']['hapi'] = {'propagate': True, 'level': 'DEBUG'} 
LOGGING['loggers']['hapi_plus'] = {'propagate': True, 'level': 'DEBUG'} 
LOGGING['loggers']['requests'] = {'propagate': True, 'level': 'DEBUG'} 


APP_DOMAIN = 'APP_DOMAIN'
API_ENV = 'qa'

HUBSPOT_MARKETPLACE_AUTH = {
    'secret_key': 'SECRET_KEY_FOR_MARKETPLACE'
}

# needed for ms sql queries
MS_ENV = 'qa'

MARKETPLACE_SLUG = 'webinars'

HUBSPOT_MARKETPLACE_MOCK_SAFETY = 'HSPY_MOCK_MIDDLEWARE'
HUBSPOT_MARKETPLACE_MOCK = {
    'slug': MARKETPLACE_SLUG,
    'app': {
        'name': 'Webinars', # override with your app name
        'callback_url': 'http://localhost:8000/webinars',
    },
}

if os.environ.get('HS_ENV')=='qa':
    MARKETPLACE_SLUG = 'webinarsqa'

settings_utils.insert_env_settings(globals())

if os.environ.get('LOCAL_DEV'):  # to force debug=True even when we're pointing at prod from local environment
    DEBUG=True
    TEMPLATE_DEBUG=True

LOCALABLE_APP_DOMAIN = ENV=='local' and 'localhost:8000' or APP_DOMAIN
LOCALABLE_APP_URL = ENV=='local' and 'http://localhost:8000' or 'https://%s' % APP_DOMAIN
APP_URL = 'https://%s' % APP_DOMAIN

ACCOUNT_SYNC_STAGE_SIZE = 10
HISTORIC_ACCOUNT_SYNC_STAGE_SIZE = 10
ACCOUNT_SYNC_SHARD_SIZE = 50
WEBEX_REGISTRANT_EVENT_SYNC_STAGE_SIZE = 500
WEBEX_ATTENDANT_EVENT_SYNC_STAGE_SIZE = 50
HUBSPOT_EVENT_SYNC_STAGE_SIZE = 100  # tried 50, but it just made things worse, cuz the chance of a single call failing is high-- so we need to reduce number of calls
EVENT_SHARD_SIZE = 30

TASK_QUEUE_AUTH = tq.Auth(53, HUBSPOT_API_KEY, env=ENV)

# Bump NUM_QUEUES if you want more work processed simultaneously. We are currently near our max
# capacity, but if more boxes are added, we can consider adding more queues.
NUM_QUEUES = 3

# Retry schedule for all taskqueues
schedule = [delta(s=20),delta(m=1),delta(m=5),delta(m=30)]

# These queues are used to process syncs.
# ...
TASK_QUEUES = [tq.Queue(
    TASK_QUEUE_AUTH, 
    name='webinarsxx_%s%s'%(ENV.lower(), x), 
    retry_schedule=schedule, 
    timeout=delta(s=60), 
    frequency=12, 
    idempotent=True) for x in range(NUM_QUEUES)]

# CONVERSION_QUEUE is the taskqueue used to create conversion events in hubspot via the leads API.
# It is a separate queue because we rely on its idempotency to prevent duplicate conversion events.
# It is used by webinars/cynq/registrant.py in HubSpotRegistrantRemoteStore._single_update().
# uid is a hexdigested hash of the form submission json. We could avoid an extra queue by slamming
# all conversion event tasks to a specific queue from the above collection, but I made a new queue 
# for better visibility into failures and delays. 
CONVERSION_QUEUE = tq.Queue(
        TASK_QUEUE_AUTH, 
        name='webinars_%s_conversion'%(ENV.lower()), 
        retry_schedule=schedule, 
        timeout=delta(s=60), 
        frequency=12, 
        idempotent=True)

