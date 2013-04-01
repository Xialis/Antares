# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def index(request):
    c = {}
    return render_to_response("accueil/index.html", c, context_instance=RequestContext(request))


def userlogout(request):
    logout(request)
    return redirect(index)
