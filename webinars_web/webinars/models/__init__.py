# gotta bubble up all SQL tables names to make Django ORM happy
from webinars_web.webinars.models.base_container_sync import BaseContainerSync
from webinars_web.webinars.models.base_sync import BaseSync
from webinars_web.webinars.models.hub_sync import HubSync
from webinars_web.webinars.models.account_sync import AccountSync
from webinars_web.webinars.models.event_sync import EventSync

from webinars_web.webinars.models.hub import Hub
from webinars_web.webinars.models.account_type import AccountType
from webinars_web.webinars.models.cms_form import CmsForm
from webinars_web.webinars.models.account import Account
from webinars_web.webinars.models.event import Event 
from webinars_web.webinars.models.event_form import EventForm
from webinars_web.webinars.models.snapshots.webex_event import WebexEventSnapshot
from webinars_web.webinars.models.snapshots.webex_registrant import WebexRegistrantSnapshot
from webinars_web.webinars.models.snapshots.gtw_event import GTWEventSnapshot
from webinars_web.webinars.models.snapshots.gtw_registrant import GTWRegistrantSnapshot
from webinars_web.webinars.models.snapshots.hubspot_registrant import HubSpotRegistrantSnapshot
from webinars_web.webinars.models.registrant import Registrant
from webinars_web.webinars.models.landing_page import LandingPage
from webinars_web.webinars.models.staged import StagedWebexRegistrant,StagedGTWRegistrant,StagedHubSpotRegistrant,StagedWebexEvent,StagedGTWEvent

from webinars_web.webinars.models.account_sync_stage import AccountSyncStage
from webinars_web.webinars.models.account_sync_shard import AccountSyncShard
from webinars_web.webinars.models.webex_event_sync_stage import WebexEventSyncStage
from webinars_web.webinars.models.gtw_event_sync_stage import GTWEventSyncStage
from webinars_web.webinars.models.hubspot_event_sync_stage import HubSpotEventSyncStage
from webinars_web.webinars.models.event_sync_shard import EventSyncShard


import dse
from django.conf import settings

import types
def dse_delete_patch(self, pk):
    "Adds a primary key to the deletion queue."
    assert type(pk) in (types.IntType,types.LongType,types.StringType,types.UnicodeType), "pk argument must be integer or long or string."
    self.delete_items.append(pk)
    self.item_counter += 1
    self._on_add()
dse.DSE.delete = dse_delete_patch

# 3.1.0 version of delete:
    #def delete(self, pk):
        #"Adds a primary key to the deletion queue."
        #assert type(pk) == types.IntType, "pk argument must be integer."
        #self.delete_items.append(pk)
        #self._on_add()

# this is fixed in 3.2 if it ever comes out in a way i can use in my app!  i really hate python
def dse_insert_patch(self, values):
    "Adds a dictionary with values to insert/update"
    self.pk_is_autofield = (self.model != CmsForm)
    if self.pk in values and self.pk_is_autofield:  # to avoid CmsForm error!
        raise dse.PrimaryKeyInInsertValues(self.pk)

    final_values = {}
    for k, v in self.default_values.items():
        if callable(v):
            final_values[k] = v()
        else:
            final_values[k] = v

    final_values.update(values)
    
    final_values = self.parse_values(final_values)
    if not final_values:
        return

    self.insert_items.append(final_values)
    self._on_add()
dse.DSE.insert = dse_insert_patch

 
# 3.1.0 version of insert:
    #def insert(self, values):
        #"Adds a dictionary with values to insert/update"
        #if self.pk in values:
            #raise PrimaryKeyInInsertValues(self.pk)

        #final_values = {}
        #for k, v in self.default_values.items():
            #if callable(v):
                #final_values[k] = v()
            #else:
                #final_values[k] = v

        #final_values.update(values)
        
        #final_values = self.parse_values(final_values)
        #if not final_values:
            #return

        #self.insert_items.append(final_values)
        #self._on_add()


def dse_generate_insert_sql_patch(self):
    self.pk_is_autofield = (self.model != CmsForm)
    sql = 'insert into %s (%s) values (%s)' % (
        self._quote(self.tablename),
        ','.join(self._quote(f) for f in self.fields if f != self.pk or not self.pk_is_autofield),
        ','.join(self.paramtoken for f in self.fields if f != self.pk or not self.pk_is_autofield),
    )
    return sql
dse.DSE._generate_insert_sql = dse_generate_insert_sql_patch


# 3.1.0 version of _generate_insert_sql:
    #def _generate_insert_sql(self):
        #sql = 'insert into %s (%s) values (%s)' % (
            #self._quote(self.tablename),
            #','.join(self._quote(f) for f in self.fields if f != self.pk),
            #','.join(self.paramtoken for f in self.fields if f != self.pk),
        #)
        #return sql

#def dse_execute_insert_statements_patch(self):
    #"Executes all bulk insert statements."
    #fieldvalues = []
    #for items in self.insert_items:
        #m = []
        #for fieldname in self.fields:
            #if fieldname in items:
                #m.append(items[fieldname])
            #elif fieldname != self.pk or not self.pk_is_autofield:
                #m.append(None)
        #fieldvalues.append(m)
        #self.records_processed += 1
    #if self.debug:
        #dse.logging.debug("Executing insert: %s" % self.insert_sql)
        #for f in fieldvalues:
            #dse.logging.debug(str(f))
    #try:
        #self._execute(self.insert_sql, fieldvalues, many=True)
    #except Exception, e:
        #raise dse.InsertManyException(e, self.tablename, self.insert_sql, fieldvalues)
#dse.DSE.execute_insert_statements = dse_execute_insert_statements_patch
        
# 3.1.0 version of execte_insert_statements:
    #def execute_insert_statements(self):
        #"Executes all bulk insert statements."
        #fieldvalues = []
        #for items in self.insert_items:
            #m = []
            #for fieldname in self.fields:
                #if fieldname in items:
                    #m.append(items[fieldname])
                #elif fieldname != self.pk or not self.pk_is_autofield:
                    #m.append(None)
            #fieldvalues.append(m)
            #self.records_processed += 1
        #if self.debug:
            #logging.debug("Executing insert: %s" % self.insert_sql)
            #for f in fieldvalues:
                #logging.debug(str(f))
        #try:
            #self._execute(self.insert_sql, fieldvalues, many=True)
        #except Exception, e:
            #raise InsertManyException(e, self.tablename, self.insert_sql, fieldvalues)

databases_hash = settings.DATABASES
settings.DATABASES = {'default': databases_hash['default']}
dse.patch_models(specific_models=[StagedWebexEvent,StagedGTWEvent,StagedWebexRegistrant,StagedGTWRegistrant,StagedHubSpotRegistrant, CmsForm, LandingPage, EventSync, EventSyncShard, AccountSyncShard, WebexRegistrantSnapshot, GTWRegistrantSnapshot, HubSpotRegistrantSnapshot, Registrant])

settings.DATABASES = databases_hash
