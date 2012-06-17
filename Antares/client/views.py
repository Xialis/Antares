# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect

from client.models import *
from client.forms import *
from client.func import ajoutClient


def index(request):
    c = {}
    listeClient = Client.objects.all()
    
    formAjoutClient = FormAjoutClient()
    formAjoutOrganisme = FormAjoutOrganisme()
    formAjoutPrescripteur = FormAjoutPrescripteur()
    
    if request.method == 'POST':
        
        if 'ajClient' in request.POST:
            retour = ajoutClient(FormAjoutClient(request.POST))
            
            if retour['b_sauver'] == False:
                formAjoutClient = retour['form']
                listeClient = Client.objects.all()
                
    
    c['listeClient'] = listeClient
    c['formAjoutClient'] = formAjoutClient
    c['formAjoutOrganisme'] = formAjoutOrganisme
    c['formAjoutPrescripteur'] = formAjoutPrescripteur
    c.update(csrf(request))
    return render_to_response("client/index.html", c)


def infoClient(request, cid):
    c = {}

    return render_to_response("client/infoClient.html", c)
