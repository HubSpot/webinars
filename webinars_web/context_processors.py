from hsdjango import bundling
from django.conf import settings
import os

def webinars_processor(request):
    """
    Load any app-specific contexts here
    """
    version = '29831234934'
    querystring_version_snippet = '?v=%s' % version
    version_snippet = '/v/%s' % version
    localable_version_snippet = version_snippet
    nonlocal_static_domain = bundling.get_static_domain()
    if settings.ENV not in ('prod','qa'):
        nonlocal_static_domain = 'sqa.com'
        localable_version_snippet = ''
    return {
        'querystring_version_snippet': querystring_version_snippet,
        'version_snippet': version_snippet,
        'nonlocal_static_domain': nonlocal_static_domain,
        'localable_version_snippet': localable_version_snippet,
        'static_domain': 'localhost:3000' if settings.ENV=='local' or os.environ.get('LOCAL_DEV') else 's.%s.com' % ('qa' if settings.ENV=='qa' else ''),
    }
