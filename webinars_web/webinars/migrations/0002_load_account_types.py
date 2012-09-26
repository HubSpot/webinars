# encoding: utf-8
from south.v2 import DataMigration
from django.core.management import call_command

class Migration(DataMigration):

    def forwards(self, orm):
        call_command("loaddata", "account_types.yaml")

    def backwards(self, orm):
        orm.AccountType.objects.all().delete()

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
