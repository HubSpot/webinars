from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound,HttpResponseForbidden
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST
from webinars_web.webinars import models
from webinars_web.webinars.forms.account import AccountForm
from marketplace.decorators import marketplace
from django.template import RequestContext
from sanetime import time, delta
from django.conf import settings
from django.utils.http import urlquote_plus
import json
import requests
import logging


@marketplace
def root(request):
    account_size = models.Account.objects.filter(hub=request.marketplace.hub_id,deleted_at__isnull=True).count()
    if account_size == 0:
        return HttpResponseRedirect('%saccounts/setup'%request.marketplace.base_url)
    else:
        return HttpResponseRedirect('%sevents'%request.marketplace.base_url) 



@marketplace
@require_GET
def list(request):
    hub = models.Hub.ensure(request.marketplace.hub_id)
    accounts = models.Account.objects.filter(hub=hub, deleted_at__isnull=True).order_by('created_at')
    if not accounts: 
        return HttpResponseRedirect('%saccounts/setup'%request.marketplace.base_url)
    return render_to_response('accounts/list.djml', {
        'accounts':accounts
    }, context_instance=RequestContext(request))

def new_or_edit(request, account_id=None, setup=False):
    from webinars_web.webinars import models as wm
    hub = models.Hub.ensure(request.marketplace.hub_id)
    kwargs = {'hub': hub}
    if account_id:
        kwargs['instance']=models.Account.objects.get(pk=account_id)
    if request.method == 'POST': # If the form has been submitted...
        if request.POST.get('cancel'):
            return HttpResponseRedirect('%saccounts'%request.marketplace.base_url) # Redirect for cancel
        if request.POST.get('account_type','1') == '2':
            redirect_uri = urlquote_plus('%s/webinars/hubs/%s/accounts/new?label=%s' % (settings.GTW_OAUTH_REDIRECT_PROTOCOL_HOST, hub.id, urlquote_plus(request.POST.get('extra',''))))
            return HttpResponseRedirect('https://api.citrixonline.com/oauth/authorize?client_id=%s&redirect_uri=%s' % (settings.GTW_API_KEY, redirect_uri))
        form = AccountForm(request.POST, **kwargs) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            if form.cleaned_data.get('account_type') == 1:
                deleted_possibles = wm.Account.objects.filter(hub=hub, username=form.cleaned_data['username'], extra=form.cleaned_data['extra'], deleted_at__isnull=False)
            elif form.cleaned_data.get('account_type') == 2:
                deleted_possibles =wm.Account.objects.filter(hub=hub, username=form.cleaned_data['username'], deleted_at__isnull=False)
            if deleted_possibles:
                account = deleted_possibles[0]
                account.deleted_at = None
                account.password = form.cleaned_data['password']
                account.exclude_old_events_from_hubspot = bool(form.cleaned_data.get('exclude_old_events_from_hubspot'))
                if account.exclude_old_events_from_hubspot:
                    ignore_delta = int(form.cleaned_data.get('exclusion_date_delta'))
                    account.exclusion_date = (time() - delta(md=ignore_delta)).us
                else:
                    account.exclusion_date = None
            else:
                account = form.save(commit=False)
            account.exclude_old_events_from_hubspot = bool(form.cleaned_data.get('exclude_old_events_from_hubspot'))
            if account.exclude_old_events_from_hubspot:
                ignore_delta = int(form.cleaned_data.get('exclusion_date_delta'))
                account.exclusion_date = (time() - delta(md=ignore_delta)).us
                print account.exclusion_date
            else:
                account.exclusion_date = None
            account.hub_id = request.marketplace.hub_id
            account.default = False
            account.prevent_unformed_lead_import = False
            account.save()
            account.hub.sync(visible=True)
            return HttpResponseRedirect('%sevents'%(request.marketplace.base_url)) # Redirect after POST
    else:
        form = AccountForm(**kwargs) # An unbound form

    return render_to_response('accounts/%s.djml'%(setup and 'setup' or account_id and 'edit' or 'new'), {
        'form': form,
        'account_types': models.AccountType.objects.all()
    }, context_instance=RequestContext(request))


def new_oauth(request, hub_id):
    from webinars_web.webinars import models as wm
    account_type = wm.AccountType.objects.get(pk=2)
    hub = wm.Hub.objects.get(pk=hub_id)
    response_key = request.GET.get('code')
    label = request.GET.get('label')
    response = requests.get('http://api.citrixonline.com/oauth/access_token?grant_type=authorization_code&code=%s&client_id=%s' % (response_key, settings.GTW_API_KEY))
    data = json.loads(response.text)
    access_token = data['access_token']
    organizer_key = data['organizer_key']
    possible_accounts = wm.Account.objects.filter(account_type=account_type, hub=hub, extra=label)
    if possible_accounts:
        account = possible_accounts[0]
        account.password = access_token
        account.username = organizer_key
    else:
        account = wm.Account(account_type=account_type, hub=hub, extra=label, password=access_token, username=organizer_key)
    account.save()
    account.hub.sync(visible=True)
    return HttpResponseRedirect('/market/%s/canvas/%s/events'% (hub_id, settings.MARKETPLACE_SLUG)) # Redirect after POST


@marketplace
def setup(request):
    return new_or_edit(request, setup=True)

@marketplace
def new(request):
    return new_or_edit(request)

@marketplace
def edit(request, account_id):
    return new_or_edit(request, account_id)


@marketplace
@require_POST
def destroy(request, account_id):
    try:
        account = models.Account.objects.get(pk=account_id)
    except:
        return HttpResponseNotFound()
    if account.hub_id != request.marketplace.hub_id:
        return HttpResponseForbidden()
    account.deleted_at = time()
    account.save()
    return HttpResponse()

def expunge(request, account_id):
    try:
        account = models.Account.objects.get(pk=account_id)
    except:
        return HttpResponseNotFound()
    account.expunge()
    return HttpResponse()



def sync(request, account_id):
    force = request.REQUEST.get('force') and True or False
    postbin = request.REQUEST.get('postbin') or None
    auto = (request.REQUEST.get('auto') is None or request.REQUEST.get('auto').lower()!='false') and True or False
    account = models.Account.objects.get(pk=account_id)
    sync_stages = account.trigger_sync(force=force, auto=auto)
    return render_to_response('accounts/trigger_sync.djml', {'account':account, 'sync_stages':sync_stages, 'postbin':postbin}, context_instance=RequestContext(request))


