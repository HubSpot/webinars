from django.shortcuts import render_to_response
from django.template import RequestContext
from webinars_web.webinars.views import syncs
from django.http import HttpResponse, HttpResponseRedirect


def show(request, sync_id):
    from webinars_web.webinars import models as wm
    account_sync = wm.AccountSync.objects.select_related('account','account__hub').get(pk=sync_id)

    events_hash = dict((e.id,e) for e in account_sync.account.events)
    event_syncs_hash = dict((es.id, es) for es in account_sync.event_syncs)
    d = {}
    for es in event_syncs_hash.values():
        es.webex_stages = []
        es.gtw_stages = []
        es.shards = []
        es.parent = account_sync
        es.event = events_hash[es.event_id]
        d[es.id] = {}
    for s in wm.WebexEventSyncStage.objects.filter(parent_sync__parent=account_sync):
        event_syncs_hash[s.parent_sync.id].webex_stages.append(s)
        s.parent_sync = event_syncs_hash[s.parent_sync.id]
    for s in wm.GTWEventSyncStage.objects.filter(parent_sync__parent=account_sync):
        event_syncs_hash[s.parent_sync.id].gtw_stages.append(s)
        s.parent_sync = event_syncs_hash[s.parent_sync.id]
    for s in wm.EventSyncShard.objects.filter(parent_sync__parent=account_sync):
        event_syncs_hash[s.parent_sync.id].shards.append(s)
        s.parent_sync = event_syncs_hash[s.parent_sync.id]
    for s in wm.HubSpotEventSyncStage.objects.filter(parent_sync__parent=account_sync).select_related('parent_sync','event_form','event_form__cms_form').order_by('start_last_modified_at','offset'):
        d[s.parent_sync.id].setdefault(s.event_form.cms_form,[]).append(s)
    for es in event_syncs_hash.values():
        es.hubspot_stages_cmsforms = [(v,k) for k,v in d[es.id].iteritems()]

    return syncs._show(request, 'account', account_sync)

def new(request, account_id):
    from webinars_web.webinars import models as wm
    return syncs._new(request, 'account', wm.Account.objects.get(pk=account_id))

def interrupt(request, account_id):
    from webinars_web.webinars import models as wm
    return syncs._interrupt(request, 'account', wm.Account.objects.get(pk=account_id))

def list(request, account_id):
    from webinars_web.webinars import models as wm
    account = wm.Account.objects.get(pk=account_id)
    account_syncs = wm.AccountSync.objects.filter(account=account, parent__isnull=True).order_by('-started_at')
    event_syncs = wm.EventSync.objects.filter(event__account=account, parent__isnull=True).order_by('-started_at')
    return render_to_response('account_syncs/list.djml', {'account':account, 'account_syncs':account_syncs, 'event_syncs':event_syncs}, context_instance=RequestContext(request))

def fill_stage(request, sync_id, stage_id):
    from webinars_web.webinars import models as wm
    return syncs._fill_stage(request, 'account', wm.AccountSyncStage.objects.get(pk=stage_id), sync_id)

def sync_shard(request, sync_id, shard_id):
    from webinars_web.webinars import models as wm
    return syncs._sync_shard(request, 'account', wm.AccountSyncShard.objects.get(pk=shard_id), sync_id)

