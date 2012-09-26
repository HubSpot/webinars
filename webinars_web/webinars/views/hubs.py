from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Min
from marketplace.decorators import marketplace
from sanetime import time,delta
from django.conf import settings
from utils.obj import ensureattr
import logging

def list(request):
    from webinars_web.webinars import models as wm
    hubs = wm.Hub.objects.select_related('current_sync','last_sync').filter().extra(
                select={'unmothballed_event_count': 'SELECT COUNT(*) FROM webinars_event e JOIN webinars_account a ON a.id=e.account_id WHERE e.mothballed=0 AND a.hub_id=webinars_hub.id'}
            ).order_by('id')
    accounts = wm.Account.objects.filter(deleted_at__isnull=True).extra(
                    select={'event_count': 'SELECT COUNT(*) FROM webinars_event WHERE webinars_event.account_id=webinars_account.id'})
    hub_map = dict((h.id,h) for h in hubs)
    for a in accounts: 
        ensureattr(hub_map[a.hub_id],'accounts_with_event_counts',[])
        hub_map[a.hub_id].accounts_with_event_counts.append(a)
    for hub in hubs:
        if hub.last_sync and hub.last_sync.completed_at:
            hub.broken = time().ms - hub.last_sync.completed_at.ms > 1000*60*60*4
        else:
            hub.broken = False
    return render_to_response('hubs/list.djml', {
        'hubs': hubs,
        'slug': settings.MARKETPLACE_SLUG
    }, context_instance=RequestContext(request))

@marketplace
def _last_synced_at(request):
    from webinars_web.webinars import models as wm
    hub = wm.Hub.ensure(request.marketplace.hub_id)
    return HttpResponse(hub.last_sync and str(hub.last_sync.completed_at.us) or '')

@marketplace
def sync(request):
    from webinars_web.webinars.views import hub_syncs
    if request.method=='POST':
        request.POST = request.POST.copy()
        request.POST.update({'visible':'True'})
    return hub_syncs.new(request, request.marketplace.hub_id)

@marketplace
def uninstall(request):
    from webinars_web.webinars import models as wm
    logging.debug('RECEIVED UNINSTALL REQUEST FOR HUB=%s' % request.marketplace.hub_id)
    hub = wm.Hub.ensure(request.marketplace.hub_id)
    hub.uninstall()
    return render_to_response('uninstalled.djml', {'hub': hub}, context_instance=RequestContext(request))

def refresh(request):
    from webinars_web.webinars import models as wm
    wm.Hub._bulk_sfdc_info_fill()
    wm.Hub._bulk_settings_fill()
    return HttpResponse("all good")

def metrics(request):
    from webinars_web.webinars import models as wm
    now = time()
    data = {}
    data['installs']=[0]*7
    data['uninstalls']=[0]*7
    data['new_mrr']=[0]*7
    data['recurring_mrr']=[0]*7
    data['months']=['Dec','Jan','Feb','Mar','Apr','May','Jun']
    for hub in wm.Hub.objects.filter(internal=False):
        if hub.friends_and_family: continue
        install_month = hub.created_at.month
        print install_month
        uninstall_month = hub.uninstalled_at and hub.uninstalled_at.month
        data['installs'][install_month%12] += 1
        if uninstall_month is not None:
            data['uninstalls'][uninstall_month%12] += 1
        if not hub.beta:
            mrr_at = hub.created_at + delta(md=30)
            new = True
            while mrr_at < now and (uninstall_month is None or mrr_at < hub.uninstalled_at):
                if new:
                    data['new_mrr'][mrr_at.month%12] += 50
                    new = False
                else:
                    data['recurring_mrr'][mrr_at.month%12] += 50
                mrr_at = mrr_at + delta(md=30)
    data['net_installs'] = []
    data['total_mrr'] = []
    for i in range(len(data['months'])):
        data['net_installs'].append(data['installs'][i]-data['uninstalls'][i])
        data['total_mrr'].append(data['new_mrr'][i]+data['recurring_mrr'][i])
    for attr in ('installs','uninstalls','net_installs','new_mrr','recurring_mrr','total_mrr'):
        data['total_%s'%attr] = sum(data[attr])
    return render_to_response('hubs/metrics.djml', { 'data': data }, context_instance=RequestContext(request))

