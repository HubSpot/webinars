# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'WebexRegistrantSnapshot.hashcode'
        db.add_column('webinars_webexregistrantsnapshot', 'hashcode', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'StagedHubSpotRegistrant.conversion_event_guid'
        db.delete_column('webinars_stagedhubspotregistrant', 'conversion_event_guid')

        # Deleting field 'StagedHubSpotRegistrant.recorded_at'
        db.delete_column('webinars_stagedhubspotregistrant', 'recorded_at')

        # Deleting field 'StagedHubSpotRegistrant.initial_form_guid'
        db.delete_column('webinars_stagedhubspotregistrant', 'initial_form_guid')

        # Adding field 'StagedHubSpotRegistrant.converted_at'
        db.add_column('webinars_stagedhubspotregistrant', 'converted_at', self.gf('sanetime.dj.SaneTimeField')(default=0), keep_default=False)

        # Adding field 'StagedHubSpotRegistrant.hashcode'
        db.add_column('webinars_stagedhubspotregistrant', 'hashcode', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'StagedHubSpotRegistrant.form_guid'
        db.add_column('webinars_stagedhubspotregistrant', 'form_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True), keep_default=False)

        # Deleting field 'HubSpotRegistrantSnapshot.conversion_event_guid'
        db.delete_column('webinars_hubspotregistrantsnapshot', 'conversion_event_guid')

        # Adding field 'HubSpotRegistrantSnapshot.hashcode'
        db.add_column('webinars_hubspotregistrantsnapshot', 'hashcode', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'EventForm.last_last_modified_at'
        db.delete_column('webinars_eventform', 'last_last_modified_at')

        # Adding field 'EventForm.last_last_converted_at'
        db.add_column('webinars_eventform', 'last_last_converted_at', self.gf('sanetime.dj.SaneTimeField')(default=0), keep_default=False)

        # Deleting field 'StagedWebexRegistrant.attended_for'
        db.delete_column('webinars_stagedwebexregistrant', 'attended_for')

        # Deleting field 'StagedWebexRegistrant.remote_id'
        db.delete_column('webinars_stagedwebexregistrant', 'remote_id')

        # Adding field 'StagedWebexRegistrant.hashcode'
        db.add_column('webinars_stagedwebexregistrant', 'hashcode', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'StagedWebexRegistrant.attendee_id'
        db.add_column('webinars_stagedwebexregistrant', 'attendee_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True), keep_default=False)

        # Adding field 'StagedWebexRegistrant.duration'
        db.add_column('webinars_stagedwebexregistrant', 'duration', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'WebexRegistrantSnapshot.hashcode'
        db.delete_column('webinars_webexregistrantsnapshot', 'hashcode')

        # Adding field 'StagedHubSpotRegistrant.conversion_event_guid'
        db.add_column('webinars_stagedhubspotregistrant', 'conversion_event_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True), keep_default=False)

        # Adding field 'StagedHubSpotRegistrant.recorded_at'
        db.add_column('webinars_stagedhubspotregistrant', 'recorded_at', self.gf('sanetime.dj.SaneTimeField')(default=0), keep_default=False)

        # Adding field 'StagedHubSpotRegistrant.initial_form_guid'
        db.add_column('webinars_stagedhubspotregistrant', 'initial_form_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True), keep_default=False)

        # Deleting field 'StagedHubSpotRegistrant.converted_at'
        db.delete_column('webinars_stagedhubspotregistrant', 'converted_at')

        # Deleting field 'StagedHubSpotRegistrant.hashcode'
        db.delete_column('webinars_stagedhubspotregistrant', 'hashcode')

        # Deleting field 'StagedHubSpotRegistrant.form_guid'
        db.delete_column('webinars_stagedhubspotregistrant', 'form_guid')

        # Adding field 'HubSpotRegistrantSnapshot.conversion_event_guid'
        db.add_column('webinars_hubspotregistrantsnapshot', 'conversion_event_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True), keep_default=False)

        # Deleting field 'HubSpotRegistrantSnapshot.hashcode'
        db.delete_column('webinars_hubspotregistrantsnapshot', 'hashcode')

        # Adding field 'EventForm.last_last_modified_at'
        db.add_column('webinars_eventform', 'last_last_modified_at', self.gf('django.db.models.fields.BigIntegerField')(default=0), keep_default=False)

        # Deleting field 'EventForm.last_last_converted_at'
        db.delete_column('webinars_eventform', 'last_last_converted_at')

        # Adding field 'StagedWebexRegistrant.attended_for'
        db.add_column('webinars_stagedwebexregistrant', 'attended_for', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'StagedWebexRegistrant.remote_id'
        db.add_column('webinars_stagedwebexregistrant', 'remote_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True), keep_default=False)

        # Deleting field 'StagedWebexRegistrant.hashcode'
        db.delete_column('webinars_stagedwebexregistrant', 'hashcode')

        # Deleting field 'StagedWebexRegistrant.attendee_id'
        db.delete_column('webinars_stagedwebexregistrant', 'attendee_id')

        # Deleting field 'StagedWebexRegistrant.duration'
        db.delete_column('webinars_stagedwebexregistrant', 'duration')


    models = {
        'webinars.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.AccountType']"}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync_job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.SyncJob']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'prevent_unformed_lead_import': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
            'deleted_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'hashcode': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync_job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.SyncJob']"}),
            'mothballed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'noshow_campaign_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'registrants_synced_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'requested_registrants_sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'started_registrants_sync_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'sync_leads_for_all_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'last_last_converted_at': ('sanetime.dj.SaneTimeField', [], {})
        },
        'webinars.hub': {
            'Meta': {'object_name': 'Hub'},
            '_attended_any_criterium_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            '_attended_any_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            '_registered_any_criterium_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            '_registered_any_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            '_timezone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'events_synced_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'requested_events_sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'started_events_sync_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'uninstalled_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'updated_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'})
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
            'conversion_event_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'deleted_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
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
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'guid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.CmsForm']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'max_size': ('django.db.models.fields.IntegerField', [], {}),
            'offset': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'sync_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.SyncJob']"})
        },
        'webinars.task': {
            'Meta': {'object_name': 'Task'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']", 'null': 'True'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'sync_all_registrants': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sync_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sync_specific_registrants': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'webinars.taskrunner': {
            'Meta': {'object_name': 'TaskRunner'},
            'completed_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
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
