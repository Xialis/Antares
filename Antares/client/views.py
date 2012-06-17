# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect

from client.models import *
from client.forms import *


def index(request):
    c = {}
    listeClient = Client.objects.all()
    
    formAjoutClient = FormAjoutClient()
    formAjoutOrganisme = FormAjoutOrganisme()
    formAjoutPrescripteur = FormAjoutPrescripteur()
    
    c['listeClient'] = listeClient
    c['formAjoutClient'] = formAjoutClient
    c['formAjoutOrganisme'] = formAjoutOrganisme
    c['formAjoutPrescripteur'] = formAjoutPrescripteur
    c.update(csrf(request))
    return render_to_response("client/index.html", c)


def infoClient(request, cid):
    c = {}

    return render_to_response("client/infoClient.html", c)
