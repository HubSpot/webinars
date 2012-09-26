# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EventForm'
        db.create_table('webinars_eventform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Event'])),
            ('cms_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.CmsForm'])),
            ('sync_start_at', self.gf('sanetime.dj.SaneTimeField')(default=0)),
        ))
        db.send_create_signal('webinars', ['EventForm'])

        db.execute("INSERT webinars_eventform (event_id, cms_form_id) SELECT event_id, cmsform_id FROM webinars_event_cms_forms");
        db.execute("INSERT webinars_eventform (event_id, cms_form_id) SELECT id, _update_cms_form_id FROM webinars_event WHERE _update_cms_form_id IS NOT NULL");

        # Deleting field 'Event._update_cms_form'
        db.delete_column('webinars_event', '_update_cms_form_id')

        # Deleting field 'Event.last_hubspot_snapshotted_at'
        db.delete_column('webinars_event', 'last_hubspot_snapshotted_at')

        # Removing M2M table for field cms_forms on 'Event'
        db.delete_table('webinars_event_cms_forms')


    def backwards(self, orm):
        # Deleting model 'EventForm'
        db.delete_table('webinars_eventform')

        # Adding field 'Event._update_cms_form'
        db.add_column('webinars_event', '_update_cms_form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['webinars.CmsForm']), keep_default=False)

        # Adding field 'Event.last_hubspot_snapshotted_at'
        db.add_column('webinars_event', 'last_hubspot_snapshotted_at', self.gf('sanetime.dj.SaneTimeField')(default=0), keep_default=False)

        # Adding M2M table for field cms_forms on 'Event'
        db.create_table('webinars_event_cms_forms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['webinars.event'], null=False)),
            ('cmsform', models.ForeignKey(orm['webinars.cmsform'], null=False))
        ))
        db.create_unique('webinars_event_cms_forms', ['event_id', 'cmsform_id'])


    models = {
        'webinars.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.AccountType']"}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'deleted_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'event_forms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webinars.CmsForm']", 'through': "orm['webinars.EventForm']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mothballed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'noshow_campaign_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'registrants_synced_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'requested_registrants_sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'started_registrants_sync_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
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
            'sync_start_at': ('sanetime.dj.SaneTimeField', [], {'default': '0'})
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
            'conversion_event_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'time_starts_at': ('sanetime.dj.SaneTimeField', [], {}),
            'timezone_starts_at': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'webinars.webexregistrantsnapshot': {
            'Meta': {'object_name': 'WebexRegistrantSnapshot'},
            'attended_for': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Event']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'started_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'stopped_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['webinars']
