"""
Local overrides for the example_web project.
"""
LOG_PATH = "/tmp/hubspot/logs"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(levelname)-5s %(name)s === %(message)s' } },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler' },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout' },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'detailed',
            'filename': 'log.log' } },
    'loggers': {
        'django.request': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': True, },
        'django.db': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propogate': True, },
        'cynq': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True, },
        'hapi_plus': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True, },
        'webex': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True, } } }

STATIC_DOMAIN = 'localhost:3000'

GTW_OAUTH_REDIRECT_PROTOCOL_HOST = 'http://qa.com:8000'

# no need for stack traces in the console if I'm seeing every one of them in the UI anyhow -- or am I-- AJAX?
DEBUG_MODE_LOGGING = False

