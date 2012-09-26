from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example_web.views.home', name='home'),
    # url(r'^example_web/', include('example_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
#    url(r'^webinars/usage/',             include('usage_tracking.urls')),
#    url(r'^example/marketplace_admin/', include('example_marketplace_admin.urls')),
    url(r'^webinars/',                   include('webinars_web.webinars.urls')),
)

