from django.db import models as djmodels
from sanetime.dj import SaneTimeField
from webinars_web.webinars.models import mixins
from sanetime import ntime,time
from utils.cast import nint


class StagedWebexEvent(djmodels.Model, mixins.Staged, mixins.Event):
    class Meta:
        app_label = 'webinars'

    account = djmodels.ForeignKey('Account')
    hashcode = djmodels.IntegerField(null=False)
    session_key = djmodels.CharField(max_length=128, null=False)
    title = djmodels.CharField(max_length=256, null=False)
    description = djmodels.CharField(max_length=2**14-1, null=True)

    _time_starts_at = SaneTimeField(null=True)
    _time_ends_at = SaneTimeField(null=True)
    _time_started_at = SaneTimeField(null=True)
    _time_ended_at = SaneTimeField(null=True)
    _timezone = djmodels.CharField(max_length=64, null=True, editable=False)

    @classmethod
    def fill(kls, account):
        from webinars_web.webinars import models as wm
        now = time()
        events = account.webex_account.events
        local_events = dict((e.remote_id, e) for e in wm.Event.objects.filter(account=account, deleted_at__isnull=True) if e.remote_id)
        with kls.delayed as d:
            for event in events:
                raw_event = dict(
                    account_id = account.id,
                    title = event.title,
                    description = event.description,
                    _timezone = event.starts_at.tz_name,
                    _time_starts_at = nint(ntime(event._starts_at)),
                    _time_ends_at = nint(ntime(event._ends_at)),
                    _time_started_at = nint(ntime(event._started_at)),
                    _time_ended_at = nint(ntime(event._ended_at)),
                    session_key  = event.session_key )

                # if customer is automatically deleting events on webex side, then we make it seem like they haven't (so we don't start pumping NULLs into ends_at and starts_at)
                local_event = local_events.get(event.session_key)
                if local_event and local_event._ends_at and now > local_event._ends_at:
                    raw_event['_time_starts_at'] = int(local_event._time_starts_at)
                    raw_event['_time_ends_at'] = int(local_event._time_ends_at)
                    raw_event['_timezone'] = local_event._timezone
                raw_event['hashcode'] = kls.calc_hashcode(**raw_event)
                d.insert(raw_event)
        from django.db import transaction
        transaction.commit_unless_managed()
        return len(events)

