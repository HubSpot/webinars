from django.db import models as djmodels
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import mixins
from utils.cast import nint,nstr

class StagedGTWEvent(djmodels.Model, mixins.Staged, mixins.Event):
    class Meta:
        app_label = 'webinars'

    account = djmodels.ForeignKey('Account')
    hashcode = djmodels.IntegerField(null=False)
    universal_key = djmodels.CharField(max_length=128, null=False)
    key = djmodels.CharField(max_length=128, null=True)
    subject = djmodels.CharField(max_length=256, null=False)
    description = djmodels.CharField(max_length=2**14-1, null=True)

    _time_starts_at = SaneTimeField(null=True)
    _time_ends_at = SaneTimeField(null=True)
    _time_started_at = SaneTimeField(null=True)
    _time_ended_at = SaneTimeField(null=True)
    _timezone = djmodels.CharField(max_length=64, null=True, editable=False)

    @classmethod
    def fill(kls, account):
        from webinars_web.webinars import models as wm
        unmothballed_past_events = dict((e.remote_id, e) for e in wm.Event.objects.filter(account=account, deleted_at__isnull=True, mothballed=False, remote_id__isnull=False))
        sessions = [s for w in account.gtw_organizer.webinars for s in w.sessions]
        with kls.delayed as d:
            for session in sessions:
                raw_event = dict(
                    account_id = account.id,
                    subject = session.webinar.subject or '',
                    description = session.webinar.description or '',
                    _timezone = session.webinar.timezone,
                    _time_starts_at = nint(session._starts_at),
                    _time_ends_at = nint(session._ends_at),
                    _time_started_at = nint(session._started_at),
                    _time_ended_at = nint(session._ended_at),
                    key = nstr(session.key),
                    universal_key  = session.universal_key )
                raw_event['hashcode'] = kls.calc_hashcode(**raw_event)
                d.insert(raw_event)
                unmothballed_past_events.pop(str(session.universal_key) or None,None)

            # if gtw event slides out of visibility (before we can mothball it) then we make it seem like it's still there (so we don't try to delete or start pumping NULLs into ends_at and starts_at)
            for k,e in unmothballed_past_events.iteritems():
                raw_event = dict(
                    account_id = e.account_id,
                    subject = e.title or '',
                    description = e.description or '',
                    _timezone = e._timezone,
                    _time_starts_at = nint(e._time_starts_at),
                    _time_ends_at = nint(e._time_ends_at),
                    _time_started_at= nint(e._time_started_at),
                    _time_ended_at = nint(e._time_ended_at),
                    key = e.alt_remote_id,
                    universal_key = e.remote_id,
                    hashcode = e.hashcode)
                d.insert(raw_event)
        from django.db import transaction
        transaction.commit_unless_managed()
        return len(sessions) + len(unmothballed_past_events)


