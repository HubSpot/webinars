from django.db import models
from sanetime.dj import SaneTimeField
from sanetime import time
from django.conf import settings
import hapi_plus.leads
from webinars_web.webinars.models import mixins


class StagedHubSpotRegistrant(models.Model, mixins.Staged):
    class Meta:
        app_label = 'webinars'

    event = models.ForeignKey('Event')
    converted_at = SaneTimeField(null=False)
    hashcode = models.IntegerField(null=False)
    email = models.CharField(max_length=64, null=False)
    first_name = models.CharField(null=True, max_length=64)
    last_name = models.CharField(null=True, max_length=64)
    lead_guid = models.CharField(null=True, max_length=36)
    form_guid = models.CharField(null=True, max_length=36)
    registered_any = models.NullBooleanField(null=True)
    registered_this = models.NullBooleanField(null=True)
    attended_any = models.NullBooleanField(null=True)
    attended_this = models.NullBooleanField(null=True)
    started_at = SaneTimeField(null=True)
    stopped_at = SaneTimeField(null=True)

    @classmethod
    def pre_stage(kls, event):  # seed this with what we've got in the snapshot, so we don't have to go through all leads each time
        super(StagedHubSpotRegistrant,kls).pre_stage(event)
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("""
INSERT webinars_stagedhubspotregistrant (event_id, converted_at, hashcode, email, first_name, last_name, lead_guid, form_guid, registered_any, registered_this, attended_any, attended_this, started_at, stopped_at)
SELECT event_id, 1, hashcode, email, first_name, last_name, lead_guid, initial_form_guid, registered_any, registered_this, attended_any, attended_this, started_at, stopped_at
FROM webinars_hubspotregistrantsnapshot WHERE event_id=%s""", [event.id])
        transaction.commit_unless_managed()



    #TODO: we still have issues with this-- cannot fix with current apis-- need to wait for new apis
    @classmethod
    def fill(kls, event, offset, start_last_modified_at, max_size, event_form):
        from webinars_web.webinars import models as wm
        leads_client = hapi_plus.leads.LeadsClient(settings.HUBSPOT_API_KEY, hub_id=event.hub.id, env=settings.API_ENV, timeout=40)
        leads = leads_client.get_leads(time_pivot='lastModifiedAt', sort='lastModifiedAt', dir='asc', start_time=start_last_modified_at.ms, form_guid=event_form.cms_form.guid, offset=offset, max=max_size)
        finish_last_modified_at = start_last_modified_at
        with kls.delayed as d:
            for lead in leads:
                added = False
                finish_last_modified_at = time(ms=lead['lastModifiedAt'])
                conversion_events = lead.get('leadConversionEvents',[])
                for conversion_event in conversion_events:
                    if conversion_event['formGuid']==event_form.cms_form.guid:
                        converted_at = time(ms=conversion_event['convertDate'])
                        if converted_at >= event_form.converted_at_cutoff:
                            reg = {'converted_at': converted_at.us}
                            for fsv in conversion_event.get('formSubmissionValues',[]):
                                name, value = (fsv['fieldName'], fsv['fieldValue'])
                                if name=='Email': reg['email'] = value.lower()
                                elif name=='FirstName': reg['first_name'] = value[:32] # cuz webex limits to 32 chars
                                elif name=='LastName': reg['last_name'] = value[:32] # cuz webex limits to 32 chars
                                elif name=='Webinars_AttendanceStartTime': reg['started_at'] = time(value).us
                                elif name=='Webinars_AttendanceStopTime': reg['stopped_at'] = time(value).us
                                elif name==event.hub.registered_any_form_key: reg['registered_any'] = value.lower()=='yes'
                                elif name==event.hub.attended_any_form_key: reg['attended_any'] = value.lower()=='yes'
                                elif name==event.registered_this_form_key: reg['registered_this'] = value.lower()=='yes'
                                elif name==event.attended_this_form_key: reg['attended_this'] = value.lower()=='yes'
                            if not reg['email']: continue
                            reg['event_id'] = event.id
                            reg['hashcode'] = wm.Registrant.calc_hashcode(reg['email'])
                            reg['lead_guid'] = lead['guid']
                            reg['form_guid'] = event_form.cms_form.guid
                            d.insert(reg)
                            added = True
                if len(conversion_events)>=10 and not added and event_form.converted_at_cutoff==0: # in case we get nothing, but know something is there somewhere, and we're definitely searching across all time
                    reg = {
                        'converted_at': 2,
                        'email': lead['email'].lower(), 
                        'first_name': lead['firstName'][:32],
                        'last_name': lead['lastName'][:32],
                        'event_id': event.id,
                        'hashcode': wm.Registrant.calc_hashcode(lead['email'].lower()),
                        'lead_guid': lead['guid'],
                        'form_guid': event_form.cms_form.guid }
                    d.insert(reg)
        from django.db import transaction
        transaction.commit_unless_managed()
        return (len(leads), finish_last_modified_at)
