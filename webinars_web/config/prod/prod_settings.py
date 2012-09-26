"""
Production overrides for the example_web Django project.
"""

# Prod-specific db's
DATABASES = {
    'default' : {
        'HOST': 'EXAMPLE_DB_HOST',
        'NAME': 'webinars',
        'USER': 'SUSR_Webinars',
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

HUBSPOT_API_KEY = '__SECRET__'

APP_DOMAIN = 'app.hubspot.com'
STATIC_DOMAIN = 's.com'
API_ENV = 'production'

# needed for ms sql queries
MS_ENV = 'prod'


HUBSPOT_MARKETPLACE_AUTH = {
    'secret_key': '__SECRET__'
}

GTW_API_KEY = '__SECRET__'
GTW_OAUTH_REDIRECT_PROTOCOL_HOST = 'https://app.hubspot.com'

MARKETPLACE_SLUG = 'webinars'

