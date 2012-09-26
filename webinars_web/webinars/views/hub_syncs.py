from django.shortcuts import render_to_response
from django.template import RequestContext
from webinars_web.webinars.views import syncs

def show(request, sync_id):
    from webinars_web.webinars import models as wm
    return syncs._show(request, 'hub', wm.HubSync.objects.select_related('hub').get(pk=sync_id))

def new(request, hub_id):
    from webinars_web.webinars import models as wm
    return syncs._new(request, 'hub', wm.Hub.objects.get(pk=hub_id))

def interrupt(request, hub_id):
    from webinars_web.webinars import models as wm
    return syncs._interrupt(request, 'hub', wm.Hub.objects.get(pk=hub_id))

def list(request, hub_id):
    from webinars_web.webinars import models as wm
    hub = wm.Hub.objects.get(pk=hub_id)
    hub_syncs = wm.HubSync.objects.filter(hub=hub).order_by('-started_at')
    account_syncs = wm.AccountSync.objects.filter(account__hub=hub, parent__isnull=True).order_by('-started_at')
    event_syncs = wm.EventSync.objects.filter(event__account__hub=hub, parent__isnull=True).order_by('-started_at')
    return render_to_response('hub_syncs/list.djml', {'hub':hub, 'hub_syncs':hub_syncs, 'account_syncs':account_syncs, 'event_syncs':event_syncs}, context_instance=RequestContext(request))


