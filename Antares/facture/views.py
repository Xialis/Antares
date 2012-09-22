# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.utils import simplejson

from client.models import Client
from client.forms import FormRechercheClient, FormAjoutClient, FormAjoutPrescription
from client.func import initFiltration, filtration

from fournisseur.forms import RechercheVerresForm
from fournisseur.func import RechercheVerres
from fournisseur.models import Type, Diametre, Traitement, Couleur

import func
from facture.forms import LigneForm


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

    # Client existant ou non ?
    if 'client_id' in request.session['appFacture']:
        # Client existant selectionné
        client = Client.objects.get(id=request.session['appFacture']['client_id'])
        formClient = FormAjoutClient(instance=client)
        b_creation = func.creationClient(False, request)
    else:
        # Nouveau Client
        b_creation = func.creationClient(True, request)

    # =============================
    # Traitement POST
    if request.method == 'POST':

        if 'ajClient' in request.POST:
            if b_creation:
                # Création d'un nouveau client
                formClient = FormAjoutClient(request.POST)
                if formClient.is_valid():
                    client = formClient.save(commit=False)
                    func.enrClient(client, request)
                    return func.etapeSuivante(request)

            else:
                # Le client existe déjà
                formClient = FormAjoutClient(request.POST, instance=client)
                if formClient.is_valid():
                    b_modif = formClient.has_changed()
                    if b_modif == True:
                        client = formClient.save(commit=False)
                        func.enrClient(client, request)
                        # On réaffiche la page pour validation modification
                        # (post modClient, pasModClient)
                    else:
                        # Le client_id est enregistré (étape précédente).
                        return func.etapeSuivante(request)

        elif 'modClient' in request.POST:
            # id du client à modifier et objet Client enregistré
            func.modificationClient(True, request)
            return func.etapeSuivante(request)

        elif 'pasModClient' in request.POST:
            # Suppresion de l'objet Client modifié
            # Utilisation du client_id
            func.modificationClient(False, request)
            func.effClient(request)
            return func.etapeSuivante(request)

    # Fin POST
    # =============================

    if b_modif:
        # Demande de confirmation, réaffichage de la page
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
        
        if 'ajPrescription' in request.POST:
            formPrescription = FormAjoutPrescription(request.POST)
            if formPrescription.is_valid():
                func.enrPrescription(request)
                return func.etapeSuivante(request)
    
    c['formPrescription'] = formPrescription
    c.update(csrf(request))
    return render_to_response("facture/etapePrescription.html", c, context_instance=RequestContext(request))


def etapeVerres(request):
    c = {}

    LigneFormSet = formset_factory(LigneForm, extra=6)
    formSetLigne = LigneFormSet()
    formSetLigne.forms[0].empty_permitted = False
    
    formRechercheVerres = RechercheVerresForm()
    
    if request.method == 'POST':
        
        if 'ajVerres' in request.POST:
            formSetLigne = LigneFormSet(request.POST)
            formSetLigne.forms[0].empty_permitted = False
            
            if formSetLigne.is_valid():
                func.enrVerres(request)
                return func.etapeSuivante(request)
            
            ''' Si le formulaire est rempli ou en partie on filtre les champs '''
            formSetLigne = LigneFormSet(request.POST)  # Si on ne refait pas un formset, le is_valid casse tout...
            formSetLigne.forms[0].empty_permitted = False
            for form in formSetLigne:
                chdata = form._get_changed_data()
                if 'vtype' in chdata:
                    form.filtre_vtype(form._raw_value('vtype'))
                
        if 'chVerres' in request.POST:
            formRechercheVerres = RechercheVerresForm(request.POST)
            c['listeRV'] = RechercheVerres(formRechercheVerres)
    
    c['formSetLigne'] = formSetLigne
    c['formRechercheVerres'] = formRechercheVerres
    c.update(csrf(request))
    return render_to_response("facture/etapeVerres.html", c, context_instance=RequestContext(request))


def ajax_filtre(request, qs=None):
    if qs is None:
        qs = []

    if request.GET.get('vtype'):
        diametres = Diametre.objects.filter(type__pk=request.GET.get('vtype'))
        couleurs = Couleur.objects.filter(type__pk=request.GET.get('vtype'))
        traitements = Traitement.objects.filter(type__pk=request.GET.get('vtype'))

    data = []
    results = []
    for choice in diametres:
        results.append((choice.pk, choice.nom))
    data.append(results)

    results = []
    for choice in couleurs:
        results.append((choice.pk, choice.nom))
    data.append(results)

    results = []
    for choice in traitements:
        results.append((choice.pk, choice.nom))
    data.append(results)

    return HttpResponse(simplejson.dumps(data))


def etapeMontures(request):
    c = {}
    
    c.update(csrf(request))
    return render_to_response("facture/etapeMontures.html", c, context_instance=RequestContext(request))
