# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EventSyncShard'
        db.create_table('webinars_eventsyncshard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_sync', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.EventSync'])),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('completed_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')()),
            ('section', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('webinars', ['EventSyncShard'])

        # Adding model 'AccountSyncStage'
        db.create_table('webinars_accountsyncstage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_sync', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.AccountSync'])),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('completed_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('offset', self.gf('django.db.models.fields.IntegerField')()),
            ('max_size', self.gf('django.db.models.fields.IntegerField')()),
            ('last', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('webinars', ['AccountSyncStage'])

        # Adding model 'HubSpotEventSyncStage'
        db.create_table('webinars_hubspoteventsyncstage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_sync', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.EventSync'])),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('completed_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('offset', self.gf('django.db.models.fields.IntegerField')()),
            ('max_size', self.gf('django.db.models.fields.IntegerField')()),
            ('last', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('webinars', ['HubSpotEventSyncStage'])

        # Adding model 'WebexEventSyncStage'
        db.create_table('webinars_webexeventsyncstage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_sync', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.EventSync'])),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('completed_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('offset', self.gf('django.db.models.fields.IntegerField')()),
            ('max_size', self.gf('django.db.models.fields.IntegerField')()),
            ('last', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('attendants', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('webinars', ['WebexEventSyncStage'])

        # Adding model 'AccountSyncShard'
        db.create_table('webinars_accountsyncshard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_sync', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.AccountSync'])),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('completed_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')()),
            ('section', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('webinars', ['AccountSyncShard'])


    def backwards(self, orm):
        
        # Deleting model 'EventSyncShard'
        db.delete_table('webinars_eventsyncshard')

        # Deleting model 'AccountSyncStage'
        db.delete_table('webinars_accountsyncstage')

        # Deleting model 'HubSpotEventSyncStage'
        db.delete_table('webinars_hubspoteventsyncstage')

        # Deleting model 'WebexEventSyncStage'
        db.delete_table('webinars_webexeventsyncstage')

        # Deleting model 'AccountSyncShard'
        db.delete_table('webinars_accountsyncshard')


    models = {
        'webinars.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.AccountType']"}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'current_sync': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.AccountSync']"}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.AccountSync']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'prevent_unformed_lead_import': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sync_lock': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'updated_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'webinars.accountsync': {
            'Meta': {'object_name': 'AccountSync'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Account']"}),
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'debug': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forced_stop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.HubSync']", 'null': 'True'}),
            'sharded_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'staged_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'webinars.accountsyncshard': {
            'Meta': {'object_name': 'AccountSyncShard'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_sync': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.AccountSync']"}),
            'section': ('django.db.models.fields.IntegerField', [], {}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        },
        'webinars.accountsyncstage': {
            'Meta': {'object_name': 'AccountSyncStage'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_size': ('django.db.models.fields.IntegerField', [], {}),
            'offset': ('django.db.models.fields.IntegerField', [], {}),
            'parent_sync': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.AccountSync']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        },
        'webinars.accounttype': {
            'Meta': {'object_name': 'AccountType'},
            'can_api_create_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_api_load_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_api_register_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_api_report_views': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'extra_username_label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'listing_priority': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'username_label': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'webinars.cmsform': {
            'Meta': {'object_name': 'CmsForm'},
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Hub']"}),
            'is_sync_target': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'webinars.event': {
            'Meta': {'object_name': 'Event'},
            '_attended_criterium_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            '_attended_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            '_noshow_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            '_registered_criterium_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            '_registered_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Account']"}),
            'attended_campaign_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'cms_forms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webinars.CmsForm']", 'through': "orm['webinars.EventForm']", 'symmetrical': 'False'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'current_sync': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.EventSync']"}),
            'deleted_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.EventSync']"}),
            'mothballed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'noshow_campaign_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'sync_leads_for_all_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sync_lock': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'time_starts_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'timezone_starts_at': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'unknowable_registrants': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'})
        },
        'webinars.eventform': {
            'Meta': {'object_name': 'EventForm'},
            'cms_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.CmsForm']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_last_converted_at': ('sanetime.dj.SaneTimeField', [], {'default': '0'})
        },
        'webinars.eventsync': {
            'Meta': {'object_name': 'EventSync'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'debug': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'forced_stop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.AccountSync']", 'null': 'True'}),
            'sharded_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'staged_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'webinars.eventsyncshard': {
            'Meta': {'object_name': 'EventSyncShard'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_sync': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.EventSync']"}),
            'section': ('django.db.models.fields.IntegerField', [], {}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        },
        'webinars.hub': {
            'Meta': {'object_name': 'Hub'},
            '_attended_any_criterium_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            '_attended_any_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            '_registered_any_criterium_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            '_registered_any_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            '_timezone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'current_sync': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.HubSync']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'last_sync': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.HubSync']"}),
            'sync_lock': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'uninstalled_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'updated_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'})
        },
        'webinars.hubspoteventsyncstage': {
            'Meta': {'object_name': 'HubSpotEventSyncStage'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_size': ('django.db.models.fields.IntegerField', [], {}),
            'offset': ('django.db.models.fields.IntegerField', [], {}),
            'parent_sync': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.EventSync']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        },
        'webinars.hubspotregistrantsnapshot': {
            'Meta': {'object_name': 'HubSpotRegistrantSnapshot'},
            'attended_any': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'attended_for': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attended_this': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_form_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'lead_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'registered_any': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'registered_this': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'stopped_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        },
        'webinars.hubsync': {
            'Meta': {'object_name': 'HubSync'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'debug': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forced_stop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'webinars.landingpage': {
            'Meta': {'object_name': 'LandingPage'},
            'cms_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.CmsForm']"}),
            'form_title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'webinars.registrant': {
            'Meta': {'object_name': 'Registrant'},
            'attended_for': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'cms_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.CmsForm']", 'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'deleted_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'lead_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'stopped_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'updated_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'})
        },
        'webinars.stagedhubspotregistrant': {
            'Meta': {'object_name': 'StagedHubSpotRegistrant'},
            'attended_any': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'attended_for': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'attended_this': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'converted_at': ('sanetime.dj.SaneTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'form_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'lead_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'registered_any': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'registered_this': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'stopped_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        },
        'webinars.stagedwebexevent': {
            'Meta': {'object_name': 'StagedWebexEvent'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Account']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'time_starts_at': ('sanetime.dj.SaneTimeField', [], {}),
            'timezone_starts_at': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'webinars.stagedwebexregistrant': {
            'Meta': {'object_name': 'StagedWebexRegistrant'},
            'attendee_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'stopped_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        },
        'webinars.syncjob': {
            'Meta': {'object_name': 'SyncJob'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Account']", 'null': 'True'}),
            'auto': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.SyncJob']", 'null': 'True'}),
            'sharded_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'staged_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'})
        },
        'webinars.syncshard': {
            'Meta': {'object_name': 'SyncShard'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.IntegerField', [], {}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'sync_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.SyncJob']"})
        },
        'webinars.syncstage': {
            'Meta': {'object_name': 'SyncStage'},
            'cms_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.CmsForm']", 'null': 'True'}),
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'max_size': ('django.db.models.fields.IntegerField', [], {}),
            'offset': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'subkind': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'sync_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.SyncJob']"})
        },
        'webinars.webexeventsnapshot': {
            'Meta': {'object_name': 'WebexEventSnapshot'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Account']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'time_starts_at': ('sanetime.dj.SaneTimeField', [], {}),
            'timezone_starts_at': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'webinars.webexeventsyncstage': {
            'Meta': {'object_name': 'WebexEventSyncStage'},
            'attendants': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_size': ('django.db.models.fields.IntegerField', [], {}),
            'offset': ('django.db.models.fields.IntegerField', [], {}),
            'parent_sync': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.EventSync']"}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        },
        'webinars.webexregistrantsnapshot': {
            'Meta': {'object_name': 'WebexRegistrantSnapshot'},
            'attended_for': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'stopped_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['webinars']
