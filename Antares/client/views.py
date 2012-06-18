# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect

from client.models import *
from client.forms import *
from client.func import ajoutClient, ajoutPrescripteur, ajoutOrganisme


def index(request):
    c = {}
    listeClient = Client.objects.all()

    formAjoutClient = FormAjoutClient()
    formAjoutOrganisme = FormAjoutOrganisme()
    formAjoutPrescripteur = FormAjoutPrescripteur()
    formRechercheClient = FormRechercheClient()

    if request.method == 'POST':

        if 'ajClient' in request.POST:
            retour = ajoutClient(FormAjoutClient(request.POST))
            listeClient = Client.objects.all()

            if retour['b_sauver'] == False:
                formAjoutClient = retour['form']

        if 'ajPrescripteur' in request.POST:
            retour = ajoutPrescripteur(FormAjoutPrescripteur(request.POST))

            if retour['b_sauver'] == False:
                formAjoutPrescripteur = retour['form']
                
        if 'ajOrganisme' in request.POST:
            retour = ajoutOrganisme(FormAjoutOrganisme(request.POST))
            
            if retour['b_sauver'] == False:
                formAjoutOrganisme = retour['form']

    c['listeClient'] = listeClient
    c['listeOrganisme'] = OrganismePayeur.objects.all()
    c['listePrescripteur'] = Prescripteur.objects.all()
    c['formAjoutClient'] = formAjoutClient
    c['formRechercheClient'] = formRechercheClient
    c['formAjoutOrganisme'] = formAjoutOrganisme
    c['formAjoutPrescripteur'] = formAjoutPrescripteur
    c.update(csrf(request))
    return render_to_response("client/index.html", c)


def infoClient(request, cid):
    c = {}

    return render_to_response("client/infoClient.html", c)
