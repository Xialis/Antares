# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext


def index(request):
    c = {}
    
    return render_to_response("facture/index.html", context_instance=RequestContext(request))
