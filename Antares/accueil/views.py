# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    c = {}
    return render_to_response("accueil/index.html", c, context_instance=RequestContext(request))
