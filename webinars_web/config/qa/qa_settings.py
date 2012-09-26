"""
QA configs for the example_web Django project
"""

# QA-specific db's
DATABASES = {
    'default': { 
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

MS_ENV = 'qa'
STATIC_DOMAIN = 'qa.com'

MARKETPLACE_SLUG = 'webinarsqa'

GTW_OAUTH_REDIRECT_PROTOCOL_HOST = 'https://qa.com'
