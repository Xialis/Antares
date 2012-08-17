# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.context_processors import csrf

from client.models import Client
from client.forms import FormRechercheClient, FormAjoutClient, FormAjoutPrescription
from client.func import initFiltration, filtration

import func


def etapeRecherche(request):
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
    return render_to_response("facture/etapeRecherche.html", c, context_instance=RequestContext(request))


def etapeInfo(request):
    c = {}
    formClient = FormAjoutClient()
    b_modif = False

    if 'client_id' in request.session['appFacture']:
        client = Client.objects.get(id=request.session['appFacture']['client_id'])
        formClient = FormAjoutClient(instance=client)
        b_creation = func.creationClient(True, request)

    ''' Traitement POST '''
    if request.method == 'POST':

        if 'ajClient' in request.POST:
            formClient = FormAjoutClient(request.POST, instance=client)
            b_modif = formClient.has_changed()
            if b_modif == True:
                func.enrClient(request)
            else:
                return func.etapeSuivante(request)

        if 'modClient' in request.POST:
            return func.etapeSuivante(request)

        if 'pasModClient' in request.POST:
            func.effClient(request)
            return func.etapeSuivante(request)

    ''' Fin POST '''

    if b_modif:
        client_orig = Client.objects.get(id=request.session['appFacture']['client_id'])
        c['client_orig'] = client_orig

    c['formClient'] = formClient
    c['b_modif'] = b_modif
    c.update(csrf(request))
    return render_to_response("facture/etapeInfo.html", c, context_instance=RequestContext(request))


def etapePrescription(request):
    c = {}
    formPrescription = FormAjoutPrescription()
    
    if request.method == 'POST':
        formPrescription = FormAjoutPrescription(request.POST)
    
    c['formPrescription'] = formPrescription
    c.update(csrf(request))
    return render_to_response("facture/etapePrescription.html", c, context_instance=RequestContext(request))
