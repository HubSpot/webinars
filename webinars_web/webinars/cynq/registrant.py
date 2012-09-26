from cynq import BaseSpec, BaseStore, DjangoStore
from webinars_web.webinars.models import WebexRegistrantSnapshot, HubSpotRegistrantSnapshot, Registrant, GTWRegistrantSnapshot
from webex.registrant import Registrant as WebexRegistrant
from gtw.registrant import Registrant as GTWRegistrant
from sanetime import time
import hapi_plus.leads
import logging
import simplejson as json
import hashlib
import hapicrank.task_queues as tq
from django.conf import settings

class WebexRegistrantSpec(BaseSpec):
    name = 'webex.registrant'
    rpushed = ('remote_id','started_at','stopped_at','ip_address')
    shared = ('email','first_name','last_name')
    key = 'email'

class GTWRegistrantSpec(BaseSpec):
    name = 'gtw.registrant'
    rpushed = ('remote_id','started_at','stopped_at')
    shared = ('email','first_name','last_name')
    key = 'email'

class HubSpotRegistrantSpec(BaseSpec):
    name = 'hubspot.registrant'
    rpushed = ('lead_guid', 'initial_form_guid')
    rpulled = ('registered_any','registered_this','attended_any','attended_this','started_at','stopped_at')
    shared = ('email','first_name','last_name')
    key = 'email'

def is_valid_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


class WebexRegistrantRemoteStore(BaseStore):
    TRANSLATION = {'remote_id':'attendee_id'}

    def __init__(self, event, shard_depth, shard_slice):
        super(WebexRegistrantRemoteStore,self).__init__()
        self.event = event
        self.shard_depth = shard_depth
        self.shard_slice = shard_slice
        self.webex_event = event.webex_event
        self.now = time()

    def _all(self):
        from webinars_web.webinars import models as wm
        #TODO: turn into webex event objects from database hashes?
        return wm.StagedWebexRegistrant.objects.filter(event=self.event).extra(where=['webinars_stagedwebexregistrant.hashcode MOD %s = %s' % (self.shard_depth, self.shard_slice)])

    def _single_create(self, dobj):
        return WebexRegistrant(self.webex_event, **dobj).create()

    def _bulk_create(self, tuples):
        valid_tuples = [t for t in tuples if is_valid_email(t[0]['email'])]
        registrants = [WebexRegistrant(self.webex_event, **t[0]) for t in valid_tuples]
        registrant_map = dict((r.email, r) for r in self.webex_event.create_registrants(registrants) if r)
        return [(tuples[i][0]['email'] in registrant_map and registrant_map[tuples[i][0]['email']].attendee_id and registrant_map[tuples[i][0]['email']] or None, tuples[i][0], tuples[i][1]) for i in xrange(len(tuples))]

    ##TODO: this does not work-- cuz there is no update method!  what would ever cause this to be called anyway!?
    #def _single_update(self, obj, dchanges):
        #for k,v in dchanges.iteritems(): setattr(obj, k, v)
        #self.controller.update(obj)
        #return obj

    #def _single_delete(self, obj):
        #self.controller.delete(obj)
        #return obj

    def _pre_cynq(self):
        return self.webex_event.session_key

    def _createable(self, arm): return self.event.ended_at > self.now
    def _updateable(self, arm): return False
    def _deleteable(self, arm): return False


class GTWRegistrantRemoteStore(BaseStore):
    TRANSLATION = {'remote_id':'key', 'stopped_at':'ended_at'}

    def __init__(self, event, shard_depth, shard_slice):
        super(GTWRegistrantRemoteStore,self).__init__()
        self.event = event
        self.shard_depth = shard_depth
        self.shard_slice = shard_slice
        self.gtw_session = event.gtw_session
        self.now = time()

    def _all(self):
        from webinars_web.webinars import models as wm
        #TODO: turn into webex event objects from database hashes?
        return wm.StagedGTWRegistrant.objects.filter(event=self.event).extra(where=['webinars_stagedgtwregistrant.hashcode MOD %s = %s' % (self.shard_depth, self.shard_slice)])

    def _single_create(self, dobj):
        return GTWRegistrant(session=self.gtw_session, webinar=self.gtw_session.webinar, **dobj).create()

    def _bulk_create(self, tuples):
        valid_tuples = [t for t in tuples if is_valid_email(t[0]['email'])]
        registrants = [GTWRegistrant(session=self.gtw_session, webinar=self.gtw_session.webinar, **t[0]) for t in valid_tuples]
        registrant_map = dict((r.email, r) for r in GTWRegistrant._create(registrants) if r)
        return [(tuples[i][0]['email'] in registrant_map and registrant_map[tuples[i][0]['email']] or None, tuples[i][0], tuples[i][1]) for i in xrange(len(tuples))]

    #def _bulk_create(self, tuples):
        #valid_tuples = [t for t in tuples if is_valid_email(t[0]['email'])]
        #registrants = [WebexRegistrant(self.webex_event, **t[0]) for t in valid_tuples]
        #registrant_map = dict((r.email, r) for r in self.webex_event.create_registrants(registrants))
        #return [(t[0]['email'] in registrant_map and registrant_map[t[0]['email']].attendee_id and registrant_map[t[0]['email']] or None, tuples[i][0], tuples[i][1]) for i in xrange(len(tuples))]

    ##TODO: this does not work-- cuz there is no update method!  what would ever cause this to be called anyway!?
    #def _single_update(self, obj, dchanges):
        #for k,v in dchanges.iteritems(): setattr(obj, k, v)
        #self.controller.update(obj)
        #return obj

    #def _single_delete(self, obj):
        #self.controller.delete(obj)
        #return obj

    def _pre_cynq(self):
        return self.gtw_session

    def _createable(self, arm): return self.event.ended_at > self.now
    def _updateable(self, arm): return False
    def _deleteable(self, arm): return False

class HubSpotRegistrant(object):
    def __init__(self):
        super(HubSpotRegistrant,self).__init__()
        for attr in HubSpotRegistrantSpec().attrs:
            setattr(self, attr, None)


class HubSpotRegistrantRemoteStore(BaseStore):
    def __init__(self, event, shard_depth, shard_slice):
        super(HubSpotRegistrantRemoteStore,self).__init__()
        self.event = event
        self.shard_depth = shard_depth
        self.shard_slice = shard_slice
        self.hub = event.hub
        self.leads_client = hapi_plus.leads.LeadsClient(event.settings.HUBSPOT_API_KEY, hub_id=self.hub.id, env=event.settings.API_ENV, timeout=20)
        self.now = time()

    def _all(self, raw_lookup=False):
        from webinars_web.webinars import models as wm
        deltas = wm.StagedHubSpotRegistrant.objects.filter(event=self.event).extra(where=['webinars_stagedhubspotregistrant.hashcode MOD %s = %s' % (self.shard_depth, self.shard_slice)]).order_by('email','converted_at')
        registrants = []
        reg = None
        last_email = None
        attrs = HubSpotRegistrantSpec().attrs
        for delta in deltas:
            if delta.email != last_email:
                if reg: registrants.append(reg)
                reg = HubSpotRegistrant()
            for attr in attrs:
                if attr == 'initial_form_guid':
                    if not reg.initial_form_guid:
                        setattr(reg, attr, delta.form_guid)
                else:
                    val = getattr(delta, attr, None)
                    if val is not None:
                        setattr(reg, attr, val)
            last_email = reg.email
        if reg: registrants.append(reg)
        return registrants

    def _single_create(self, dobj):
        return self._single_update(HubSpotRegistrant(), dobj)

    def _single_update(self, obj, dchanges):
        for k,v in dchanges.iteritems(): setattr(obj, k, v)
        value_list = ( ('email', ('Email Address', 'Email')), 
                ('first_name', ('First Name', 'FirstName')), 
                ('last_name', ('Last Name', 'LastName')), 
                ('registered_any', (self.hub.registered_any_form_label, self.hub.registered_any_form_key)), 
                ('registered_this', (self.event.registered_this_form_label, self.event.registered_this_form_key)), 
                ('attended_any', (self.hub.attended_any_form_label, self.hub.attended_any_form_key)), 
                ('attended_this', (self.event.attended_this_form_label, self.event.attended_this_form_key)), 
                ('duration', ('Attendance Duration', 'Webinars_AttendanceDuration')),
            ('started_at', ('Attendence Start Time', 'Webinars_AttendanceStartTime')),
            ('stopped_at', ('Attendence Stop Time', 'Webinars_AttendanceStopTime')) )
        form_values = []
        for k,v in value_list:
            if (k in dchanges.keys() or k=='email') and getattr(obj,k) is not None:
                if k.endswith('_at'):
                    form_values.append({
                        'fieldLabel':v[0],
                        'fieldName':v[1],
                        'fieldValue':time(getattr(obj,k).us,self.hub.timezone).strftime("%a %b %d, %Y %H:%M:%S %Z")})
                elif k.endswith('_any') or k.endswith('_this'):
                    form_values.append({
                        'fieldLabel':v[0],
                        'fieldName':v[1],
                        'fieldValue':getattr(obj,k) and 'YES' or 'NO'})
                elif k == 'duration':
                    form_values.append({
                        'fieldLabel':v[0],
                        'fieldName':v[1],
                        'fieldValue':'%s minutes' % getattr(obj,k).m})
                else:
                    form_values.append({
                        'fieldLabel':v[0],
                        'fieldName':v[1],
                        'fieldValue':getattr(obj,k)})
        #self.leads_client.create_lead(self.event.update_cms_form.guid, form_values)
        data = json.dumps(dict(
            formSubmissionValues = form_values,
            portalId = self.hub.id,
            formGuid = self.event.update_cms_form.guid
            ))
        # the conversion queue is idempotent. we never want the same form submitted more than once.
        # ...
        uid = hashlib.sha256(data).hexdigest()
        _url = "https://api.hubapi%s.com/create-lead?portalId=%s&hapikey=%s" % (
                "" if settings.API_ENV.lower() in ["prod", "production"] else "qa",
                self.hub.id,
                settings.HUBSPOT_API_KEY
                )
        # We can also use settings.TASK_QUEUES[self.event.id % settings.NUM_QUEUES]
        # because self.event.id % settings.NUM_QUEUES will always use the same queue
        # for a specific event.
        # The current queue is helpful for debugging though, since it is not cluttered
        # with other webinars work.
        task = tq.Task(
                queue=settings.CONVERSION_QUEUE, 
                method="POST", 
                url=_url, 
                body=data, 
                content_type="application/json",
                uid=uid
                ).enqueue(max_retries=5)
        logging.debug("TQDEBUG: conversion event registered with task_queue system :: %s" % task)
        logging.debug("TQDEBUG: task body \n ::\n%s\n::\n" % task.body)
        logging.debug("TQDEBUG: task uid : %s" % uid)
        logging.debug("conversion for event: %s" % self.event.id)
        obj.initial_form_guid = obj.initial_form_guid or self.event.update_cms_form.guid
        return obj

    def _deleteable(self, arm): return False



class RegistrantDjangoStore(DjangoStore):
    def __init__(self, event, shard_depth, shard_slice):
        super(RegistrantDjangoStore, self).__init__()
        self.event = event
        self.shard_depth = shard_depth
        self.shard_slice = shard_slice
        self.now = time()

    def _all(self): 
        return self.django_klass.objects.select_related('event').filter(event = self.event)
    
    def _single_create(self, dobj):
        dobj = dobj.copy()
        dobj['hashcode'] = Registrant.calc_hashcode(dobj['email'])
        dobj['event'] = self.event
        return super(RegistrantDjangoStore, self)._single_create(dobj)

    def _bulk_create(self, tuples):
        with self.django_klass.delayed as d:
            for t in tuples:
                payload = dict(hashcode=Registrant.calc_hashcode(t[0]['email']), event_id=self.event.id, **t[0])
                if payload.get('started_at',None): payload['started_at'] = int(payload['started_at'])
                if payload.get('stopped_at',None): payload['stopped_at'] = int(payload['stopped_at'])
                d.insert(payload)
        from django.db import transaction
        transaction.commit_unless_managed()
        registrant_map = dict((r.email,r) for r in self.django_klass.objects.filter(event = self.event))
        return [(tuples[i][0]['email'] in registrant_map and registrant_map[tuples[i][0]['email']] or None, tuples[i][0], tuples[i][1]) for i in xrange(len(tuples))]

class WebexRegistrantSnapshotStore(RegistrantDjangoStore):
    django_klass = WebexRegistrantSnapshot

    def _all(self): 
        return self.django_klass.objects.filter(event=self.event).extra(where=['webinars_webexregistrantsnapshot.hashcode MOD %s = %s' % (self.shard_depth, self.shard_slice)])

class GTWRegistrantSnapshotStore(RegistrantDjangoStore):
    django_klass = GTWRegistrantSnapshot

    def _all(self): 
        return self.django_klass.objects.filter(event=self.event).extra(where=['webinars_gtwregistrantsnapshot.hashcode MOD %s = %s' % (self.shard_depth, self.shard_slice)])

class HubSpotRegistrantSnapshotStore(RegistrantDjangoStore):
    django_klass = HubSpotRegistrantSnapshot

    def _all(self): 
        return self.django_klass.objects.filter(event=self.event).extra(where=['webinars_hubspotregistrantsnapshot.hashcode MOD %s = %s' % (self.shard_depth, self.shard_slice)])


class RegistrantLocalStore(RegistrantDjangoStore):
    django_klass = Registrant

    def _all(self): 
        return self.django_klass.objects.select_related('event','update_cms_form').filter(event=self.event, deleted_at__isnull=True).extra(where=['webinars_registrant.hashcode MOD %s = %s' % (self.shard_depth, self.shard_slice)])
    
    def _single_delete(self, obj):
        return self._single_update(obj, {'deleted_at': time()})

    def _deleteable(self, arm): return False

    def _bulk_create(self, tuples):
        with self.django_klass.delayed as d:
            for t in tuples:
                payload = dict(hashcode=Registrant.calc_hashcode(t[0]['email']), event_id=self.event.id, created_at=self.now.us, updated_at=self.now.us, **t[0])
                if payload.get('started_at',None): payload['started_at'] = int(payload['started_at'])
                if payload.get('stopped_at',None): payload['stopped_at'] = int(payload['stopped_at'])
                d.insert(payload)
        from django.db import transaction
        transaction.commit_unless_managed()
        registrant_map = dict((r.email,r) for r in self.django_klass.objects.filter(event = self.event))
        return [(tuples[i][0]['email'] in registrant_map and registrant_map[tuples[i][0]['email']] or None, tuples[i][0], tuples[i][1]) for i in xrange(len(tuples))]


