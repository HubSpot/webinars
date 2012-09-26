from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from sanetime import time,delta
from django.db.models import Min

def _show(request, trigger_model_name, sync):
    return render_to_response('%s_syncs/show.djml'%(trigger_model_name,), {'sync':sync}, context_instance=RequestContext(request))

def _new(request, trigger_model_name, trigger_object):
    # can't use REQUEST cuz I'm modifying POST or GET in some cases, and REQUEST doesn't like that
    force = (request.GET.get('force',None) or request.POST.get('force','False')).lower()=='true'
    visible = (request.GET.get('visible',None) or request.POST.get('visible','False')).lower()=='true'
    debug = (request.GET.get('debug',None) or request.POST.get('debug',request.method == 'POST' and 'False' or 'True')).lower()=='true'
    sync = trigger_object.sync(debug=debug, force=force, visible=visible)
    if request.method == 'POST': return HttpResponse()
    return HttpResponseRedirect('/webinars/%s_syncs/%s' % (trigger_model_name, sync.id))

def _interrupt(request, trigger_model_name, trigger_object):
    trigger_object.shutdown_all_syncs()
    return HttpResponseRedirect('/webinars/%ss/%s/syncs' % (trigger_model_name, trigger_object.id))

def _fill_stage(request, trigger_model_name, stage, sync_id):
    stage.go()
    if request.method == 'POST': return HttpResponse()
    return HttpResponseRedirect('/webinars/%s_syncs/%s'%(trigger_model_name, sync_id))

def _sync_shard(request, trigger_model_name, shard, sync_id):
    shard.go()
    if request.method == 'POST': return HttpResponse()
    return HttpResponseRedirect('/webinars/%s_syncs/%s'%(trigger_model_name, sync_id))

def stats(request):
    return render_to_response('syncs/stats.djml', {
        'parcel_snapshot_counts': _parcel_snapshot_counts(),
        'times': _parcel_timings(),
    }, context_instance=RequestContext(request))

def _parcel_snapshot_counts():
    from webinars_web.webinars import models as wm
    now = time()
    models = [wm.AccountSyncStage, wm.AccountSyncShard, wm.HubSpotEventSyncStage, wm.WebexEventSyncStage, wm.EventSyncShard]
    awaiting_work, working, worked, wait_time, work_time = ([],[],[],[],[])
    for m in models:
        awaiting_work.append(m.objects.filter(completed_at__isnull=True, started_at__isnull=True, parent_sync__debug=False).count())
        working.append(m.objects.filter(completed_at__isnull=True, started_at__isnull=False, parent_sync__debug=False).count())
        worked.append(m.objects.filter(completed_at__isnull=False, parent_sync__debug=False, parent_sync__forced_stop=False).count())
        wait_time.append(now - (m.objects.filter(completed_at__isnull=True, started_at__isnull=True, parent_sync__debug=False).aggregate(Min('created_at'))['created_at__min'] or now))
        work_time.append(now - (m.objects.filter(completed_at__isnull=True, started_at__isnull=False, parent_sync__debug=False).aggregate(Min('started_at'))['started_at__min'] or now))
    return (sum(awaiting_work), sum(working), sum(worked), max(wait_time).ms, max(work_time).ms)

def _parcel_timings():
    from webinars_web.webinars import models as wm
    now = time()
    time_chunks = {'hour':10**6*60**2, 'day':10**6*60**2*24, 'week':10**6*60**2*24*7}
    since_times = dict((k,now-v) for k,v in time_chunks.iteritems())
    times = dict((k,{'wait':[], 'work':[]}) for k,v in time_chunks.iteritems())
    min_since_time = min(since_times.values())
    models = (wm.AccountSyncStage, wm.AccountSyncShard, wm.HubSpotEventSyncStage, wm.WebexEventSyncStage, wm.EventSyncShard)
    for m in models:
        for created_at, started_at, completed_at in m.objects.filter(created_at__isnull=False, created_at__gt=min_since_time, parent_sync__debug=False, parent_sync__forced_stop=False).values_list('created_at','started_at','completed_at'):
            for k in time_chunks.keys():
                if created_at >= since_times[k] and started_at:
                    times[k]['wait'].append(time(started_at)-time(created_at))
                    if completed_at:
                        times[k]['work'].append(time(completed_at)-time(started_at))
    for k in times.keys():
        for t in ('wait','work'):
            lst = times[k][t]
            times[k][t] = len(lst)>0 and ((sum(lst,delta(0))/len(lst)).ms, min(lst).ms, max(lst).ms) or (None,None,None)
    return times

