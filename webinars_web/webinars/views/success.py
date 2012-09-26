import os
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET
from django.template import RequestContext
from marketplace.decorators import marketplace

@marketplace
@require_GET
def guide(request):
    return render_to_response('success_guide.djml', {}, context_instance=RequestContext(request))
