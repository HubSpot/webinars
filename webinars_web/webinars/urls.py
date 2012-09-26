from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('webinars_web.webinars.views',
    # Examples:
    url(r'^$', 'accounts.root'),

    url(r'^accounts$', 'accounts.list'),
    url(r'^accounts/new$', 'accounts.new'),
    url(r'^accounts/(?P<account_id>\d+)/edit$', 'accounts.edit'),
    url(r'^accounts/(?P<account_id>\d+)/destroy$', 'accounts.destroy'),
    url(r'^accounts/(?P<account_id>\d+)/expunge$', 'accounts.expunge'),

    url(r'^accounts/setup$', 'accounts.setup'),

    url(r'^hubs/(?P<hub_id>\d+)/accounts/new$', 'accounts.new_oauth'),

    url(r'^events$', 'events.list'),
    url(r'^eventsx/(?P<event_id>\d+)/(?P<segment>\w+)', 'events.export'),
    url(r'^events/_(?P<which>\w+)$', 'events._list'),
    url(r'^events/new$', 'events.new'),
    url(r'^events/(?P<event_id>\d+)$', 'events.show'),
    url(r'^events/(?P<event_id>\d+)/edit$', 'events.edit'),
    url(r'^events/(?P<event_id>\d+)/destroy$', 'events.destroy'),

    #url(r'^accounts/(?P<account_id>\d+)/sync', 'accounts.sync'),

    #url(r'^sync_stages/(?P<sync_stage_id>\d+)/fill', 'sync_stages.fill'),

    url(r'^events/(?P<event_id>\d+)/registrants$', 'registrants.list'),

    url(r'^status$', 'public.status'),
    url(r'^boot$', 'public.boot'),
    url(r'^about$', 'public.about'),
    url(r'^faq$', 'public.faq'),
    url(r'^hubs/uninstall$', 'hubs.uninstall'),

    url(r'^success_guide$', 'success.guide'),

    url(r'^syncs/update$', 'public.sync_all'),
    url(r'^syncs/new$', 'hubs.sync'),
    url(r'^syncs/_last_synced_at', 'hubs._last_synced_at'),

    url(r'^hubs/(?P<hub_id>\d+)/syncs/new$', 'hub_syncs.new'),
    url(r'^accounts/(?P<account_id>\d+)/syncs/new$', 'account_syncs.new'),
    url(r'^events/(?P<event_id>\d+)/syncs/new', 'event_syncs.new'),
    
    url(r'^hub_syncs/(?P<sync_id>\d+)$', 'hub_syncs.show'),
    url(r'^account_syncs/(?P<sync_id>\d+)$', 'account_syncs.show'),
    url(r'^event_syncs/(?P<sync_id>\d+)$', 'event_syncs.show'),

    url(r'^account_syncs/(?P<sync_id>\d+)/stages/(?P<stage_id>\d+)/go', 'account_syncs.fill_stage'),
    url(r'^account_syncs/(?P<sync_id>\d+)/shards/(?P<shard_id>\d+)/go', 'account_syncs.sync_shard'),

    url(r'^event_syncs/(?P<sync_id>\d+)/kickoff', 'event_syncs.kickoff'),
    url(r'^event_syncs/(?P<sync_id>\d+)/webex_stages/(?P<stage_id>\d+)/go', 'event_syncs.fill_webex_stage'),
    url(r'^event_syncs/(?P<sync_id>\d+)/gtw_stages/(?P<stage_id>\d+)/go', 'event_syncs.fill_gtw_stage'),
    url(r'^event_syncs/(?P<sync_id>\d+)/hubspot_stages/(?P<stage_id>\d+)/go', 'event_syncs.fill_hubspot_stage'),
    url(r'^event_syncs/(?P<sync_id>\d+)/shards/(?P<shard_id>\d+)/go', 'event_syncs.sync_shard'),

    url(r'^hubs/(?P<hub_id>\d+)/syncs/interrupt$', 'hub_syncs.interrupt'),
    url(r'^hubs/(?P<hub_id>\d+)/syncs', 'hub_syncs.list'),
    url(r'^hubs$', 'hubs.list'),
    url(r'^syncs$', 'syncs.stats'),
    url(r'^metrics$', 'hubs.metrics'),

    url(r'^accounts/(?P<account_id>\d+)/syncs/interrupt$', 'account_syncs.interrupt'),
    url(r'^accounts/(?P<account_id>\d+)/syncs', 'account_syncs.list'),
    url(r'^accounts$', 'accounts.list_all'),

    url(r'^events/(?P<event_id>\d+)/syncs/interrupt$', 'event_syncs.interrupt'),
    url(r'^events/(?P<event_id>\d+)/syncs', 'event_syncs.list'),
    url(r'^events$', 'events.list_all'),

    url(r'^hubs/refresh$', 'hubs.refresh')

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
