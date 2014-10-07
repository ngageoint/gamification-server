# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Badge

def overview(request, extra_context={}):
    badges = Badge.objects.active().order_by("level")
    
    context = locals()
    context.update(extra_context)
    return render_to_response("badges/overview.html", context, context_instance=RequestContext(request))

def detail(request, slug, extra_context={}):
    badge = get_object_or_404(Badge, id=slug)
    users = badge.user.all()
    
    context = locals()
    context.update(extra_context)
    return render_to_response("badges/detail.html", context, context_instance=RequestContext(request))