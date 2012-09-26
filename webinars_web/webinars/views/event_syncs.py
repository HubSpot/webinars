from django.shortcuts import render_to_response
from django.template import RequestContext
from webinars_web.webinars.views import syncs
from django.http import HttpResponse, HttpResponseRedirect

def show(request, sync_id):
    from webinars_web.webinars import models as wm
    event_sync = wm.EventSync.objects.select_related('event','parent','event__account','event__account__hub').get(pk=sync_id)
    for c in ['webex_stages','gtw_stages','shards']:
        for s in getattr(event_sync,c):
            s.parent_sync = event_sync
    return syncs._show(request, 'event', event_sync)

def new(request, event_id):
    from webinars_web.webinars import models as wm
    return syncs._new(request, 'event', wm.Event.objects.get(pk=event_id))

def interrupt(request, event_id):
    from webinars_web.webinars import models as wm
    return syncs._interrupt(request, 'event', wm.Event.objects.get(pk=event_id))

def list(request, event_id):
    from webinars_web.webinars import models as wm
    event = wm.Event.objects.get(pk=event_id)
    event_syncs = wm.EventSync.objects.filter(event=event, parent__isnull=True).order_by('-started_at')
    return render_to_response('event_syncs/list.djml', {'event':event, 'event_syncs':event_syncs}, context_instance=RequestContext(request))

def fill_webex_stage(request, sync_id, stage_id):
    from webinars_web.webinars import models as wm
    return syncs._fill_stage(request, 'event', wm.WebexEventSyncStage.objects.get(pk=stage_id), sync_id)

def fill_gtw_stage(request, sync_id, stage_id):
    from webinars_web.webinars import models as wm
    return syncs._fill_stage(request, 'event', wm.GTWEventSyncStage.objects.get(pk=stage_id), sync_id)

def fill_hubspot_stage(request, sync_id, stage_id):
    from webinars_web.webinars import models as wm
    stage= wm.HubSpotEventSyncStage.objects.get(pk=stage_id)
    return syncs._fill_stage(request, 'event', stage, sync_id)

def sync_shard(request, sync_id, shard_id):
    from webinars_web.webinars import models as wm
    return syncs._sync_shard(request, 'event', wm.EventSyncShard.objects.get(pk=shard_id), sync_id)

def kickoff(request, sync_id):
    from webinars_web.webinars import models as wm
    event_sync = wm.EventSync.objects.get(pk=sync_id)
    event_sync.start()
    if request.method == 'POST': return HttpResponse()
    return HttpResponseRedirect('/webinars/event_syncs/%s'%event_sync.id)


