import os
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings
from webinars_web.webinars import models
import requests
from gtw import Organizer

@require_GET
def status(request):
    #latest_task_runners = models.TaskRunner.objects.filter(completed_at__isnull=False, started_at__gt=sanetime().us-10**6*60**2*12).order_by('-started_at')
    #task_runner_started_at = long(request.GET.get('task_runner_started_at') or latest_task_runners[0].started_at)
    #task_runner_completed_at = long(request.GET.get('task_runner_completed_at') or latest_task_runners[0].completed_at)
    #latest_tasks = models.Task.objects.filter(started_at__gt=task_runner_started_at, started_at__lt=task_runner_completed_at).order_by('started_at')
    [x.register() for x in settings.TASK_QUEUES]
    settings.CONVERSION_QUEUE.register()
    return render_to_response('status.djml', {
        #'latest_tasks': latest_tasks,
        #'latest_task_runners': latest_task_runners,
        #'average_duration_last12':(sum([(tr.completed_at-tr.started_at) for tr in latest_task_runners])/(60*12)+5*10**5)/10**6
    })

@require_GET
def boot(request):
    return HttpResponseRedirect('/webinars/status')

@require_GET
def style_guide(request):
    raw_text = open(os.path.join(os.path.dirname(__file__), '../templates/style_guide.djml')).read()
    return HttpResponse(raw_text)

@require_GET
def about(request):
    return render_to_response('about.djml', {}, context_instance=RequestContext(request))

@require_GET
def faq(request):
    return render_to_response('faq.djml', {}, context_instance=RequestContext(request))

# POST request expected, GET request assumed to be debugging request
def sync_all(request):
    from webinars_web.webinars import models as wm
    syncs = wm.Hub.sync_all()
    if request.method == 'POST':
        return HttpResponse()
    return render_to_response('hubs/sync_all.djml', {'syncs': syncs}, context_instance=RequestContext(request))
