from operator import attrgetter
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponseForbidden
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST
from webinars_web.webinars.forms.event import EventForm
from marketplace.decorators import marketplace
from sanetime import time
from django.conf import settings
import hapi.leads
#from django.core import management
from django.template import RequestContext
from webinars_web.webinars import utils
import csv
import logging

def bucket_events(hub):
    from webinars_web.webinars import models as wm
    events = wm.Event.objects.filter(
            account__hub=hub, deleted_at__isnull=True).select_related('current_sync','account').extra(
                    select={'registrant_count': 'SELECT COUNT(*) FROM webinars_registrant WHERE webinars_registrant.event_id=webinars_event.id'}).extra(
                    select={'attendant_count': 'SELECT COUNT(*) FROM webinars_registrant WHERE webinars_registrant.event_id=webinars_event.id AND started_at IS NOT NULL'})
    events = sorted(events, key=attrgetter('starts_at'), reverse=True)
    event_ids_form_ids = [(ef.event_id, ef.cms_form_id) for ef in  wm.EventForm.objects.filter(event__in=wm.Event.objects.filter(account__hub=hub, deleted_at__isnull=True), cms_form__is_sync_target=False)]
    event_id_to_form_ids_map = {}
    for event_id, form_id in event_ids_form_ids:
        event_id_to_form_ids_map.setdefault(event_id,[]).append(form_id)
    form_ids_lps = [(lp.cms_form_id, lp) for lp in wm.LandingPage.objects.filter(cms_form__in=set(ef[1] for ef in event_ids_form_ids))]
    form_id_to_lp_map = {}
    for form_id, lp in form_ids_lps:
        form_id_to_lp_map.setdefault(form_id,[]).append(lp)
    for event in events: #TODO: this is creating an 2N+1 situation-- need to refactor!
        event.landing_pages = []
        for form_id in event_id_to_form_ids_map.get(event.id,[]):
            event.landing_pages.extend(form_id_to_lp_map[form_id])

    now = time()
    return utils.partition(events, lambda e: (e.ended_at < now), [True,False])

@marketplace
@require_GET
def _list(request, which):  # returns the partial list requested (future or past)-- used by ajax table replace
    from webinars_web.webinars import models as wm
    hub = wm.Hub.ensure(request.marketplace.hub_id)
    buckets = bucket_events(hub)
    is_future = which.lower()=='future'
    is_past = not is_future
    return render_to_response('events/_list.djml', {
        'events': buckets[is_past],
        'past': is_past,
        'empty_callout': is_future
    }, context_instance=RequestContext(request))

@marketplace
@require_GET
def list(request):
    from webinars_web.webinars import models as wm
    hub = wm.Hub.ensure(request.marketplace.hub_id, select_related=['current_sync','last_sync'])
    buckets = bucket_events(hub)
    return render_to_response('events/list.djml', {
        'future_events': buckets[False],
        'past_events': buckets[True],
        'hub': hub,
    }, context_instance=RequestContext(request))

def filter_registrants(registrants, segment):
    if segment == 'noshows': return [r for r in registrants if not r.get('started_at')]
    elif segment == 'attendees': return [r for r in registrants if r.get('started_at')]
    else: return registrants

@marketplace
@require_GET
def export(request, event_id, segment):
    if segment not in ['noshows', 'attendees', 'registrants']: return HttpResponseForbidden()
    attrs = ['first_name', 'last_name', 'email']
    
    from webinars_web.webinars import models as wm
    registrant_set = wm.Event.objects.filter(pk=event_id)[0].registrant_set.values()
    logging.debug('CSVDEBUG: event=%s, segment=%s' % (event_id, segment))
    name = '%s%s' % (segment, event_id)
    logging.debug('CSVDEBUG: filename=%s' % name)
    people = filter_registrants(registrant_set, segment)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % name

    writer = csv.writer(response)
    writer.writerow(['FirstName', 'LastName', 'Email'])
    for p in people:
        writer.writerow([p.get(attr).encode('utf-8') for attr in attrs])
    return response


def get_fresh_last_modified_at(hub, guid):
    leads_client = hapi.leads.LeadsClient(settings.HUBSPOT_API_KEY, hub_id=hub.id, env=settings.API_ENV)
    leads = leads_client.get_leads(
            time_pivot = 'lastModifiedAt',
            sort = 'lastModifiedAt',
            dir = 'desc',
            max = 1,
            form_guid = guid)
    if leads:
        return time(us=leads[0]['lastModifiedAt']*1000 + 1000)
    else:
        return time(0)

def new_or_edit(request, event_id=None):
    from webinars_web.webinars import models as wm
    hub = wm.Hub.ensure(request.marketplace.hub_id)
    kwargs = {'hub':hub}
    old_sync_leads_for_all_time = None
    if event_id:
        kwargs['instance']=wm.Event.objects.select_related('account').get(pk=event_id)
        old_sync_leads_for_all_time = kwargs['instance'].sync_leads_for_all_time
    if request.method == 'POST': # If the form has been submitted...
        form = EventForm(request.POST, **kwargs) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            event = form.save(commit=False)
            tz = kwargs.get('instance') and kwargs['instance'].starts_at.tz or hub.timezone
            event.starts_at = time(form.cleaned_data['starts_at_ndt'], tz)
            event.duration = int(form.cleaned_data['duration'])
            event.ensure_hashcode()
            event.save()
            old_cms_forms = dict((cf.guid, cf) for cf in event.cms_forms.all())
            new_cms_forms = dict((cf.guid, cf) for cf in form.cleaned_data['cms_forms'])
            for guid in (set(new_cms_forms) - set(old_cms_forms)):
                wm.EventForm.objects.create(cms_form=new_cms_forms[guid], event=event, last_last_modified_at = not event.sync_leads_for_all_time and get_fresh_last_modified_at(hub, guid) or 0, converted_at_cutoff = not event.sync_leads_for_all_time and time() or 0)
            for guid in (set(old_cms_forms) - set(new_cms_forms)):
                wm.EventForm.objects.filter(cms_form=old_cms_forms[guid], event=event).delete() 
            if old_sync_leads_for_all_time is not None and old_sync_leads_for_all_time != event.sync_leads_for_all_time:
                for event_form in event.eventform_set.all():
                    if event.sync_leads_for_all_time:
                        event_form.last_last_modified_at = 0
                        event_form.converted_at_cutoff = 0
                        # doing the else doesn't really make sense cuz we could've already been syncing before
                        event_form.save()
            return HttpResponseRedirect('%sevents'%request.marketplace.base_url) # Redirect after POST
    else:
        wm.CmsForm.sync(hub)
        form = EventForm(**kwargs) # An unbound form

    return render_to_response('events/%s.djml'%(event_id and 'edit' or 'new'), {
        'form': form,
    }, context_instance=RequestContext(request))

@marketplace
def new(request):
    return new_or_edit(request)

@marketplace
def edit(request, event_id):
    return new_or_edit(request, event_id)


@marketplace
@require_POST
def destroy(request, event_id):
    from webinars_web.webinars import models as wm
    try:
        event = wm.Event.objects.get(pk=event_id)
    except Exception:
        return HttpResponseNotFound()
    if event.account.hub_id != request.marketplace.hub_id:
        return HttpResponseForbidden()
    event.deleted_at = time()
    event.save()
    return HttpResponse()

@marketplace
def show(request, event_id):
    from webinars_web.webinars import models as wm
    hub = wm.Hub.ensure(request.marketplace.hub_id)

    try:
        event = wm.Event.objects.select_related('account','account__hub').get(pk=event_id)
    except:
        return HttpResponseNotFound()
    if event.account.hub_id != hub.id:
        return HttpResponseForbidden()

    registrants = event.registrant_set.select_related('cms_form').extra(
        select = { 'durationx': 'IF(ISNULL(stopped_at) OR ISNULL(started_at), NULL, stopped_at-started_at)' },
        order_by = ['-durationx']
    )
    for r in registrants:
        r.event = event
    lps = [lp for lp in wm.LandingPage.objects.filter(cms_form__event=event)]
    forms_to_lps = {}
    for lp in lps:
        forms_to_lps.setdefault(lp.cms_form.guid,[]).append(lp)
    for r in registrants:
        if r.effective_duration:
            if not r.cms_form or r.cms_form.is_sync_target:
                r.landing_pages = []
            else:
                r.landing_pages = forms_to_lps[r.cms_form.guid]

    now = time()
    if event._time_ended_at or event.ends_at < now:
        partitioned_registrants = utils.partition(registrants, lambda r: bool(r.started_at and r.stopped_at), [True, False])
        return render_to_response('events/show.djml', {
            'event': event,
            'future': False,
            'registrants': registrants,
            'registrants_count': len(registrants),
            'attendees': partitioned_registrants[True],
            'attendees_count': len(partitioned_registrants[True]),
            'noshows': partitioned_registrants[False],
            'noshows_count': len(partitioned_registrants[False]),
            'MARKETPLACE_SLUG': settings.MARKETPLACE_SLUG,
        }, context_instance=RequestContext(request))
    else:
        return render_to_response('events/show.djml', {
            'event': event,
            'future': True,
            'registrants': registrants,
            'registrants_count': len(registrants),
            'MARKETPLACE_SLUG': settings.MARKETPLACE_SLUG,
        }, context_instance=RequestContext(request))


def sync(request, event_id):
    from webinars_web.webinars import models as wm
    force = request.REQUEST.get('force') and True or False
    postbin = request.REQUEST.get('postbin') or None
    auto = (request.REQUEST.get('auto') is None or request.REQUEST.get('auto').lower()!='false') and True or False
    event = wm.Event.objects.get(pk=event_id)
    sync_stages = event.trigger_sync(force=force, auto=auto)
    return render_to_response('events/trigger_sync.djml', {'event':event, 'sync_stages':sync_stages, 'postbin':postbin}, context_instance=RequestContext(request))


