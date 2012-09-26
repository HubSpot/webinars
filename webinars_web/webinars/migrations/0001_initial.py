# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Hub'
        db.create_table('webinars_hub', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, primary_key=True)),
            ('started_events_sync_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('events_synced_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('requested_events_sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timezone', self.gf('django.db.models.fields.CharField')(default='America/New_York', max_length=64)),
            ('uninstalled_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('registered_any_criterium_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('attended_any_criterium_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('registered_any_saved_search_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('attended_any_saved_search_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('updated_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('avoid_lead_update_on_unformed_events', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('webinars', ['Hub'])

        # Adding model 'AccountType'
        db.create_table('webinars_accounttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username_label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('extra_username_label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('listing_priority', self.gf('django.db.models.fields.IntegerField')()),
            ('can_api_create_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_api_load_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_api_register_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('can_api_report_views', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
        ))
        db.send_create_signal('webinars', ['AccountType'])

        # Adding model 'CmsForm'
        db.create_table('webinars_cmsform', (
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('is_sync_target', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Hub'])),
        ))
        db.send_create_signal('webinars', ['CmsForm'])

        # Adding model 'Account'
        db.create_table('webinars_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.AccountType'])),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=64)),
            ('extra_username', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Hub'])),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
        ))
        db.send_create_signal('webinars', ['Account'])

        # Adding model 'Event'
        db.create_table('webinars_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Account'])),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('time_starts_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('timezone_starts_at', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('attended_campaign_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('noshow_campaign_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('_update_cms_form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['webinars.CmsForm'])),
            ('started_registrants_sync_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('registrants_synced_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('requested_registrants_sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('avoid_sync', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_hubspot_snapshotted_at', self.gf('sanetime.dj.SaneTimeField')(default=0)),
            ('updated_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('deleted_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
        ))
        db.send_create_signal('webinars', ['Event'])

        # Adding M2M table for field cms_forms on 'Event'
        db.create_table('webinars_event_cms_forms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['webinars.event'], null=False)),
            ('cmsform', models.ForeignKey(orm['webinars.cmsform'], null=False))
        ))
        db.create_unique('webinars_event_cms_forms', ['event_id', 'cmsform_id'])

        # Adding model 'WebexEventSnapshot'
        db.create_table('webinars_webexeventsnapshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Account'])),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('time_starts_at', self.gf('sanetime.dj.SaneTimeField')()),
            ('timezone_starts_at', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('webinars', ['WebexEventSnapshot'])

        # Adding model 'WebexRegistrantSnapshot'
        db.create_table('webinars_webexregistrantsnapshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Event'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('stopped_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('attended_for', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
        ))
        db.send_create_signal('webinars', ['WebexRegistrantSnapshot'])

        # Adding model 'HubSpotRegistrantSnapshot'
        db.create_table('webinars_hubspotregistrantsnapshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Event'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('lead_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('conversion_event_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('initial_form_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('registered_any', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('registered_this', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('attended_any', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('attended_this', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('stopped_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('attended_for', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('webinars', ['HubSpotRegistrantSnapshot'])

        # Adding model 'Registrant'
        db.create_table('webinars_registrant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Event'])),
            ('remote_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('conversion_event_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('lead_guid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('attended_for', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('cms_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.CmsForm'], null=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('stopped_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('updated_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('deleted_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
        ))
        db.send_create_signal('webinars', ['Registrant'])

        # Adding model 'LandingPage'
        db.create_table('webinars_landingpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cms_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.CmsForm'])),
            ('form_title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('webinars', ['LandingPage'])

        # Adding model 'TaskRunner'
        db.create_table('webinars_taskrunner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('completed_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
        ))
        db.send_create_signal('webinars', ['TaskRunner'])

        # Adding model 'Task'
        db.create_table('webinars_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Hub'])),
            ('sync_events', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webinars.Event'], null=True)),
            ('sync_all_registrants', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sync_specific_registrants', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True)),
            ('created_at', self.gf('sanetime.dj.SaneTimeField')(blank=True)),
            ('started_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
            ('completed_at', self.gf('sanetime.dj.SaneTimeField')(null=True)),
        ))
        db.send_create_signal('webinars', ['Task'])


    def backwards(self, orm):
        
        # Deleting model 'Hub'
        db.delete_table('webinars_hub')

        # Deleting model 'AccountType'
        db.delete_table('webinars_accounttype')

        # Deleting model 'CmsForm'
        db.delete_table('webinars_cmsform')

        # Deleting model 'Account'
        db.delete_table('webinars_account')

        # Deleting model 'Event'
        db.delete_table('webinars_event')

        # Removing M2M table for field cms_forms on 'Event'
        db.delete_table('webinars_event_cms_forms')

        # Deleting model 'WebexEventSnapshot'
        db.delete_table('webinars_webexeventsnapshot')

        # Deleting model 'WebexRegistrantSnapshot'
        db.delete_table('webinars_webexregistrantsnapshot')

        # Deleting model 'HubSpotRegistrantSnapshot'
        db.delete_table('webinars_hubspotregistrantsnapshot')

        # Deleting model 'Registrant'
        db.delete_table('webinars_registrant')

        # Deleting model 'LandingPage'
        db.delete_table('webinars_landingpage')

        # Deleting model 'TaskRunner'
        db.delete_table('webinars_taskrunner')

        # Deleting model 'Task'
        db.delete_table('webinars_task')


    models = {
        'webinars.account': {
            'Meta': {'object_name': 'Account'},
            'account_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.AccountType']"}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '64'}),
            'extra_username': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Hub']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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
            '_update_cms_form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['webinars.CmsForm']"}),
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webinars.Account']"}),
            'attended_campaign_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'avoid_sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cms_forms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webinars.CmsForm']", 'symmetrical': 'False'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'deleted_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_hubspot_snapshotted_at': ('sanetime.dj.SaneTimeField', [], {'default': '0'}),
            'noshow_campaign_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'registrants_synced_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'requested_registrants_sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'started_registrants_sync_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'time_starts_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'timezone_starts_at': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'updated_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'})
        },
        'webinars.hub': {
            'Meta': {'object_name': 'Hub'},
            'attended_any_criterium_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'attended_any_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'avoid_lead_update_on_unformed_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('sanetime.dj.SaneTimeField', [], {'blank': 'True'}),
            'events_synced_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'registered_any_criterium_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True'}),
            'registered_any_saved_search_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'requested_events_sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'started_events_sync_at': ('sanetime.dj.SaneTimeField', [], {'null': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'America/New_York'", 'max_length': '64'}),
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
