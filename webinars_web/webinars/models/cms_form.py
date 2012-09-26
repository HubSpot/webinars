from django.db import models
from hubspot import pool
from sanetime import time

# all forms that are actually tied to a legit landing page
SQL_ALL_FORMS = ""
SQL_ALL_FORMS_FOR_HUB_ID = ""
SQL_ALL_FORMS_FOR_FORM_GUID = ""

# all forms that are actually tied to an external landing page with submissions in the past 30 days
SQL_ALL_EXTERNAL_FORMS = """"""

class CmsForm(models.Model):
    class Meta:
        app_label = 'webinars'

    guid = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=256)
    is_sync_target = models.BooleanField(default=False)
    hub = models.ForeignKey('Hub')

    @classmethod
    def sync(kls, hub):
        from webinars_web.webinars import models as wm

        # get local info
        local_map = {}
        for lp in wm.LandingPage.objects.select_related('cms_form').filter(cms_form__hub=hub, cms_form__is_sync_target=False):
            guid = lp.cms_form.guid
            local_map.setdefault(guid, {'cms_form':lp.cms_form, 'lps':{}})
            local_map[guid]['lps'][lp.url] = lp
        local_set = set(local_map)


        #get remote info
        remote_map={}
        with pool.init():
            conn = pool.get_ms(hub.id)
            rows = conn.select(SQL_ALL_FORMS_FOR_HUB_ID, (hub.id,))
            rows_external = conn.select(SQL_ALL_EXTERNAL_FORMS, (hub.id,))
            rows.extend(rows_external)
            for row in rows:
                guid = str(row['FormGuid']).strip()
                remote_map.setdefault(guid, {'cms_form_name':row['FormName'][:256], 'lps':{}})
                url = row['PageUrl'][:128].split('?')[0]
                remote_map[guid]['lps'][url] = {'name':row['PageName'][:64], 'form_title':row['FormTitle'] and row['FormTitle'][:64]}

        remote_set = set(remote_map)

        #after remote load

        with wm.CmsForm.delayed as cms_dse:
            with wm.LandingPage.delayed as lp_dse:

                for guid in wm.CmsForm.objects.filter(hub=hub, is_sync_target=False).values_list('guid', flat=True):
                    if guid not in local_set:
                        cms_dse.delete(guid)

                # purge deleted forms/lps
                for guid in local_set-remote_set:
                    for url,local_lp in local_map[guid]['lps'].iteritems():
                        lp_dse.delete(local_lp.id)
                    cms_dse.delete(guid)

                # purge deleted lps
                for guid in remote_set&local_set:
                    for url in set(local_map[guid]['lps'])-set(remote_map[guid]['lps']):
                        lp_dse.delete(local_map[guid]['lps'][url].id)


        with wm.LandingPage.delayed as lp_dse:
            with wm.CmsForm.delayed as cms_dse:

                # add new forms/lps
                for guid in remote_set-local_set:
                    cms_dse.insert({'guid':guid, 'name':remote_map[guid]['cms_form_name'], 'is_sync_target':False, 'hub_id':hub.id})
                    for url, remote_lp_info in remote_map[guid]['lps'].iteritems():
                        remote_lp_info['cms_form_id'] = guid
                        remote_lp_info['url'] = url
                        lp_dse.insert(remote_lp_info)

                # updates
                for guid in remote_set&local_set:
                    # update change form names
                    if local_map[guid]['cms_form'].name != remote_map[guid]['cms_form_name']:
                        cms_dse.update({'guid':guid, 'name':remote_map[guid]['cms_form_name']})

                    # add new lps
                    for url in set(remote_map[guid]['lps'])-set(local_map[guid]['lps']):
                        remote_lp_info = remote_map[guid]['lps'][url]
                        remote_lp_info['cms_form_id'] = guid
                        remote_lp_info['url'] = url
                        lp_dse.insert(remote_lp_info)

                    # update lp changes
                    for url in set(remote_map[guid]['lps'])&set(local_map[guid]['lps']):
                        remote_lp_info = remote_map[guid]['lps'][url]
                        local_lp = local_map[guid]['lps'][url]
                        if local_lp.name != remote_lp_info['name'] or local_lp.form_title != remote_lp_info['form_title']:
                            remote_lp_info['cms_form_id'] = guid
                            remote_lp_info['id'] = local_lp.id
                            lp_dse.update(remote_lp_info)



        from django.db import transaction
        transaction.commit_unless_managed()


