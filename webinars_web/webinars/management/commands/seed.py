from django.core.management.base import BaseCommand
from optparse import make_option
from webinars_web.webinars import models as wm
from uuid import uuid4
from webex.attendee import Attendee as WebexRegistrant
import hapi_plus.leads
from django.conf import settings

class Command(BaseCommand):
    help = 'Seeds registrant data for an event'
    option_list = BaseCommand.option_list + (

        make_option('-e', '--event', type='int', dest='event_id', help=
                'The local id for a specific webinar event to seed.'),

        make_option('-w', '--webex_count', type='int', dest='webex_count', help=
                'Number of Webex registrants to seed on this event'),

        make_option('-s', '--hubspot_count', type='int', dest='hubspot_count', help=
                'Number of HubSpot registrants to seed on this event') )


    def handle(self, *args, **options):
        event_id = options.get('event_id')
        webex_count = options.get('webex_count') or 0
        hubspot_count = options.get('hubspot_count') or 0
        event = wm.Event.objects.get(pk=event_id)

        print "bulk inserting %s webex registrants" % webex_count
        webex_event = event.webex_event
        event.webex_event.create_registrants(WebexRegistrant.random(webex_event, webex_count))

        leads_client = hapi_plus.leads.LeadsClient(settings.HUBSPOT_API_KEY, hub_id=event.hub.id, env=settings.API_ENV, timeout=20)
        print "incrementally inserting %s hubspot registrants" % hubspot_count
        for i in xrange(hubspot_count):
            form_values = []
            form_values.append({'fieldLabel':'Email Address', 'fieldName':'Email', 'fieldValue': ('%s@%s.com' % (str(uuid4())[:8], str(uuid4())[:8]))})
            form_values.append({'fieldLabel':'First Name', 'fieldName':'FirstName', 'fieldValue': str(uuid4())[:8]})
            form_values.append({'fieldLabel':'Last Name', 'fieldName':'LastName', 'fieldValue': str(uuid4())[:8]})
            leads_client.create_lead(event.update_cms_form.guid, form_values)
            print "inserted %s hubspot registrants" % i

