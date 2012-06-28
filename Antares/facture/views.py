# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.context_processors import csrf

from client.forms import FormRechercheClient
from client.func import initFiltration, filtration

def index(request):
    c = {}
    
    formRechercheClient = FormRechercheClient()
    
    riF = initFiltration(request)
    if riF['b_listeFiltree']:
        b_listeFiltree = True
        formRechercheClient = FormRechercheClient(riF['posted'])
    else:
        b_listeFiltree = False
        
    if request.method == 'POST':
        
        if 'reClient' in request.POST:

            retour = filtration(request)
            b_listeFiltree = retour['b_listeFiltree']
            if b_listeFiltree == True:
                formRechercheClient = FormRechercheClient(request.POST)
            else:
                formRechercheClient = FormRechercheClient()
    
    c['formRechercheClient'] = formRechercheClient
    c.update(csrf(request))
    return render_to_response("facture/index.html", c, context_instance=RequestContext(request))
