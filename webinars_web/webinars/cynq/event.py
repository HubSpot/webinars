from cynq import BaseSpec, BaseStore, DjangoStore
from webinars_web.webinars.models import WebexEventSnapshot, Event, GTWEventSnapshot
from sanetime import time
from webex.event import Event as WebexEvent


class WebexEventSpec(BaseSpec):
    name = 'webex.event'
    rpushed = ('remote_id','_started_at','_ended_at')
    shared = ('title','description','_starts_at','_ends_at')
    key = 'remote_id'

class GTWEventSpec(BaseSpec):
    name = 'gtw.event'
    rpushed = ('remote_id','alt_remote_id','_starts_at','_ends_at','_started_at','_ended_at','title','description')
    shared = ()
    key = 'remote_id'


class WebexEventRemoteStore(BaseStore):
    TRANSLATION = {'remote_id':'session_key'}

    def __init__(self, account, shard_depth, shard_slice):
        super(WebexEventRemoteStore,self).__init__()
        self.account = account
        self.shard_depth = shard_depth
        self.shard_slice = shard_slice
        self.webex_account = self.account.webex_account
        self.now = time()

    def _all(self):
        from webinars_web.webinars import models as wm
        #TODO: turn into webex event objects from database hashes?
        return wm.StagedWebexEvent.objects.raw('SELECT * FROM webinars_stagedwebexevent WHERE account_id=%s AND hashcode MOD %s = %s', [self.account.id, self.shard_depth, self.shard_slice])

    def _single_create(self, dobj):
        event = WebexEvent(self.webex_account, **dobj)
        if event.starts_at > self.now: 
            return event.create()
        raise StandardError("can't create an event set for the past")

    def _single_update(self, obj, dchanges):
        for k,v in dchanges.iteritems(): setattr(obj, k, v)
        event = WebexEvent(self.webex_account, **obj.__dict__)
        if event.starts_at > self.now: 
            return event.update()
        raise StandardError("can't create an event set for the past")

    def _single_delete(self, obj):
        event = WebexEvent(self.webex_account, **obj.__dict__)
        return event.delete()

class GTWEventRemoteStore(BaseStore):
    TRANSLATION = {'remote_id':'universal_key', 'title':'subject', 'alt_remote_id':'key'}

    def __init__(self, account, shard_depth, shard_slice):
        super(GTWEventRemoteStore,self).__init__()
        self.account = account
        self.shard_depth = shard_depth
        self.shard_slice = shard_slice
        self.organizer = self.account.gtw_organizer
        self.now = time()

    def _all(self):
        from webinars_web.webinars import models as wm
        #TODO: turn into gtw event objects from database hashes?
        return wm.StagedGTWEvent.objects.raw('SELECT * FROM webinars_stagedgtwevent WHERE account_id=%s AND hashcode MOD %s = %s', [self.account.id, self.shard_depth, self.shard_slice])

    def _createable(self, arm): return False
    def _updateable(self, arm): return False
    def _deleteable(self, arm): return False


class EventDjangoStore(DjangoStore):
    def __init__(self, account, shard_depth, shard_slice):
        super(EventDjangoStore, self).__init__()
        self.account = account
        self.shard_depth = shard_depth
        self.shard_slice = shard_slice

    def _single_create(self, dobj):
        dobj = dobj.copy()
        dobj['hashcode'] = Event.calc_hashcode(**dobj)
        dobj['account'] = self.account
        return super(EventDjangoStore, self)._single_create(dobj)

    def _single_update(self, obj, dchanges):
        dchanges = dchanges.copy()
        if dchanges.get('remote_id'):
            dchanges['hashcode'] = Event.calc_hashcode(**dchanges)
        return super(EventDjangoStore, self)._single_update(obj, dchanges)
            

class WebexEventSnapshotStore(EventDjangoStore):
    django_klass = WebexEventSnapshot

    def _all(self): 
        return self.django_klass.objects.raw('SELECT * FROM webinars_webexeventsnapshot WHERE account_id=%s AND hashcode MOD %s = %s', [self.account.id, self.shard_depth, self.shard_slice])
    

class GTWEventSnapshotStore(EventDjangoStore):
    django_klass = GTWEventSnapshot

    def _all(self): 
        return self.django_klass.objects.raw('SELECT * FROM webinars_gtweventsnapshot WHERE account_id=%s AND hashcode MOD %s = %s', [self.account.id, self.shard_depth, self.shard_slice])
    

class EventLocalStore(EventDjangoStore):
    django_klass = Event

    def __init__(self, *args, **kwargs):
        super(EventLocalStore, self).__init__(*args,**kwargs)
        self.now = time()

    def _all(self): 
        return self.django_klass.objects.raw('SELECT * FROM webinars_event WHERE account_id=%s AND deleted_at IS NULL AND hashcode MOD %s = %s', [self.account.id, self.shard_depth, self.shard_slice])
    
    def _single_delete(self, obj):
        if obj.starts_at > self.now:
            return self._single_update(obj, {'deleted_at': time()})
        raise StandardError("can't delete an event locally that's in the past")

    def _deleteable(self, arm):
        return arm and arm.spec and arm.spec.name == 'webex.event' or False


