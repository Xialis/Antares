# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist

from client.models import Client, Prescription
from client.forms import FormRechercheClient, FormAjoutClient, FormAjoutPrescription, FormAjoutPrescripteur

#from client.func import initFiltration, filtration, sauvClient
import client.func as cfunc

from fournisseur.models import Type, Diametre, Traitement, Couleur

from stock.models import LigneStock

import func
from facture.forms import LigneForm, MontureForm, OptionForm, ChoixFactureForm
from facture.models import Interlocuteur


def etapeRecherche(request):
    c = {}

    formRechercheClient = FormRechercheClient()

    riF = cfunc.initFiltration(request)
    if riF['b_listeFiltree']:
        b_listeFiltree = True
        formRechercheClient = FormRechercheClient(riF['posted'])
    else:
        b_listeFiltree = False

    if request.method == 'POST':

        if 'reClient' in request.POST:

            retour = cfunc.filtration(request)
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
    formClient = None
    b_modif = False

    # =============================
    # Restauration sur GET
    if request.method == 'GET' and 'appFacture' in request.session:
        saf = request.session['appFacture']

        if 'client' in saf:
            # On a déjà les infos du client (nouveau ou modif sur existant)
            b_creation = saf['b_creation']
            formClient = FormAjoutClient(instance=saf['client'])
            if b_creation:
                b_modif = False
            else:
                b_modif = True

    # Fin restauration
    # =============================

    # Client existant ou non ?
    if 'client_id' in request.session['appFacture'] and formClient is None:
        # Client existant selectionné
        client = Client.objects.get(id=request.session['appFacture']['client_id'])
        formClient = FormAjoutClient(instance=client)
        b_creation = func.creationClient(False, request)
    elif formClient is None:
        # Nouveau Client
        formClient = FormAjoutClient()
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
    formAjoutPrescripteur = FormAjoutPrescripteur(prefix="ajPrescripteur")
    if request.session['appFacture']['client_id']:
        c['listePrescriptions'] = Prescription.objects.filter(client=request.session['appFacture']['client_id'])

    # ============================
    # Restauration
    if request.method == 'GET' and 'appFacture' in request.session:

        prescription = func.getPrescription(request)
        if prescription is not None:
            formPrescription = FormAjoutPrescription(instance=prescription)
    # Fin restauration
    # ============================

    if request.method == 'POST':

        if 'ajPrescription' in request.POST:
            formPrescription = FormAjoutPrescription(request.POST)
            if formPrescription.is_valid():
                prescription = formPrescription.save(commit=False)
                func.enrPrescription(prescription, request)
                return func.etapeSuivante(request)

        elif 'ajPrescripteur-nom' in request.POST:
            formAjoutPrescripteur = FormAjoutPrescripteur(request.POST, prefix="ajPrescripteur")
            if formAjoutPrescripteur.is_valid():
                formAjoutPrescripteur.save()
                #On recharge le formulaire de prescription
                formPrescription = FormAjoutPrescription()
                formAjoutPrescripteur = FormAjoutPrescripteur(prefix="ajPrescripteur")

    c['formPrescription'] = formPrescription
    c['formAjoutPrescripteur'] = formAjoutPrescripteur
    c.update(csrf(request))
    return render_to_response("facture/etapePrescription.html", c, context_instance=RequestContext(request))


# ==
# Etape verre
#
def etapeVerres(request):
    c = {}

    LigneFormSet = formset_factory(LigneForm, extra=6)
    formSetLigne = LigneFormSet()
    formSetLigne.forms[0].empty_permitted = False

    # ============================
    # Restauration
    if request.method == 'GET' and 'appFacture' in request.session:
        if 'etapeVerres_post' in request.session['appFacture']:
            formSetLigne = LigneFormSet(request.session['appFacture']['etapeVerres_post'])
            formSetLigne.forms[0].empty_permitted = False
            for form in formSetLigne:
                chdata = form._get_changed_data()
                if 'vtype' in chdata:
                    form.filtre_vtype(form._raw_value('vtype'))
    # Fin restauration
    # ============================

    if request.method == 'POST':

        if 'ajVerres' in request.POST:
            formSetLigne = LigneFormSet(request.POST)
            formSetLigne.forms[0].empty_permitted = False

            # On charge les choix disponibles pour validation...
            for form in formSetLigne:
                chdata = form._get_changed_data()
                if 'vtype' in chdata:
                    form.filtre_vtype(form._raw_value('vtype'))

            if formSetLigne.is_valid():
                func.enrVerres(formSetLigne, request)
                return func.etapeSuivante(request)

            # Si le formulaire est rempli ou en partie on filtre les champs
            formSetLigne = LigneFormSet(request.POST)  # Si on ne refait pas un formset, le is_valid casse tout...
            formSetLigne.forms[0].empty_permitted = False
            for form in formSetLigne:
                chdata = form._get_changed_data()
                if 'vtype' in chdata:
                    form.filtre_vtype(form._raw_value('vtype'))

    c['formSetLigne'] = formSetLigne
    c.update(csrf(request))
    return render_to_response("facture/etapeVerres.html", c, context_instance=RequestContext(request))


def ajax_filtre(request, qs=None):
    if qs is None:
        qs = []

    if request.GET.get('vtype'):
        id_vtype = request.GET.get('vtype')
    else:
        return HttpResponse(simplejson.dumps([]))

    diametres = Diametre.objects.filter(type__pk=id_vtype)
    couleurs = Couleur.objects.filter(type__pk=id_vtype)
    traitements = Traitement.objects.filter(type__pk=id_vtype)

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


def ajax_info(request, qs=None):
    data = []

    if request.GET.get('vtype') == '' or request.GET.get('diametre') == '':
        return HttpResponse(simplejson.dumps([["ERR"]]))

    id_vtype = request.GET.get('vtype')
    vtype = Type.objects.get(pk=id_vtype)

    if vtype.stock == True:
        id_diametre = request.GET.get('diametre')
        id_couleur = request.GET.get('couleur')
        id_traitement = request.GET.get('traitement')

        if id_couleur == '':
            id_couleur = None

        if id_traitement == '':
            id_traitement = None

        prescription = request.session['appFacture']['prescription']

        oeil = request.GET.get('oeil').lower()

        sphere = prescription.__getattribute__('sphere_' + oeil)
        cylindre = prescription.__getattribute__('cylindre_' + oeil)
        if cylindre == None:
            cylindre = 0

        try:
            ls = LigneStock.objects.get(vtype__pk=id_vtype,
                                        diametre__pk=id_diametre,
                                        couleur__pk=id_couleur,
                                        traitement__pk=id_traitement,
                                        sphere=sphere,
                                        cylindre=cylindre
                                        )

        except ObjectDoesNotExist:
            quantite = -1
        else:
            quantite = ls.quantite
            if quantite < 0:
                quantite = 0

        data = ['stock', quantite]

    else:
        data = ['prescription', 0]

    return HttpResponse(simplejson.dumps(data))


# ==
# Etape Montures
#
def etapeMontures(request):
    c = {}
    nbreMonture = func.getNbreMontures(request)
    MontureFormSet = formset_factory(MontureForm, extra=nbreMonture)
    formSetMonture = MontureFormSet()
    for f in formSetMonture:
        f.empty_permitted = False

    # ============================
    # Restauration
    if request.method == 'GET' and 'appFacture' in request.session:
        if 'etapeMontures_post' in request.session['appFacture']:
            formSetMonture = MontureFormSet(request.session['appFacture']['etapeMontures_post'])
            for f in formSetMonture:
                f.empty_permitted = False
    # Fin restauration
    # ============================

    if request.method == 'POST':

        if 'ajMontures' in request.POST:
            formSetMonture = MontureFormSet(request.POST)
            for f in formSetMonture:
                f.empty_permitted = False

            if formSetMonture.is_valid():
                func.enrMontures(formSetMonture, request)
                return func.etapeSuivante(request)

    c['formSetMonture'] = formSetMonture
    c.update(csrf(request))
    return render_to_response("facture/etapeMontures.html", c, context_instance=RequestContext(request))


# ==
# Etape Options
#
def etapeOptions(request):
    c = {}

    OptionFormSet = formset_factory(OptionForm)
    formSetOption = OptionFormSet()
    # ============================
    # Restauration
    if request.method == 'GET' and 'appFacture' in request.session:
        if 'etapeOptions_post' in request.session['appFacture']:
            formSetOption = OptionFormSet(request.session['appFacture']['etapeOptions_post'])
    # Fin restauration
    # ============================
    if request.method == 'POST':

        if 'ajOption' in request.POST:
            formSetOption = OptionFormSet(request.POST)
            if formSetOption.is_valid():
                func.enrOptions(formSetOption, request)
                return func.etapeSuivante(request)

    c['formSetOption'] = formSetOption
    c.update(csrf(request))
    return render_to_response("facture/etapeOptions.html", c, context_instance=RequestContext(request))


# ==
# Etape Recapitulatif
#
def etapeRecapitulatif(request):
    c = {}
    s_aF = request.session['appFacture']
    formFacture = ChoixFactureForm()
    dico_client = func.getClient(request)
    client_orig = None

    if dico_client['client'] == None:
        client = Client.objects.get(id=dico_client['client_id'])
    else:
        client = dico_client['client']
        if dico_client['client_id']:
            client_orig = Client.objects.get(id=dico_client['client_id'])

    t_verres = func.getVerres(request)
    t_options = func.getOptions(request)
    t_montures = func.getMontures(request)
    prescription = func.getPrescription(request)
    prescription_t = func.getPrescription_T(request)

    if request.method == 'POST':
        '''
        Enregistrement du client (s'il n'existe pas)
        ou Enregistrement des modifications (s'il y en a)
        Enregistrement de la prescrition
        Enregistrement de la Facture (génération ID)
        Enregistrement LigneFacture (verres)
        Enregistrement Monture(s)
        Enregistrement Options
        Si stock : traitement / Si "à commander" traitement.
        Reset assistant
        '''

        # Traitement client (-> client.id)
        if s_aF['b_creation'] == True:
            client = func.getClient(request)
            client = cfunc.sauvClient(client)
        elif 'b_modification' in s_aF and s_aF['b_modification'] == True:
            client = func.getClient(request)
            client_orig = Client.objects.get(id=dico_client['client_id'])

            client_orig.nom = client.nom
            client_orig.prenom = client.prenom
            client_orig.telephone = client.telephone
            client_orig.email = client.email
            client = client_orig.save()
        else:
            client = Client.objects.get(id=dico_client['client_id'])

        # Traitement de la prescription
        prescription = func.getPrescription(request)
        prescription.client = client
        prescription.save()

        # Traitement Facture (-> facture.id)
        formFacture = ChoixFactureForm(request.POST)
        formFacture.is_valid()
        facture = formFacture.save(commit=False)
        facture.client = client
        facture.prescription = prescription
        facture.interlocuteur = Interlocuteur.objects.get(id=1)  # TODO: gerer l'interlocuteur
        func.sauvFacture(facture)

        # Traitement LigneFacture
        t_lignes = func.getVerres(request)
        for ligne in t_lignes:
            ligne.facture = facture
            ligne.save()

        # Traitement monture(s)
        t_montures = func.getMontures(request)
        for monture in t_montures:
            monture.facture = facture
            monture.save()

        # Traitement option(s)
        t_options = func.getOptions(request)
        for option in t_options:
            option.facture = facture
            option.save()

        # Traitement stock/commande
        
        return func.reset(request)

    c['client'] = client
    c['client_orig'] = client_orig
    c['t_verres'] = t_verres
    c['t_options'] = t_options
    c['t_montures'] = t_montures
    c['prescription'] = prescription
    c['prescription_t'] = prescription_t
    c['formFacture'] = formFacture
    c.update(csrf(request))
    return render_to_response("facture/etapeRecapitulatif.html", c, context_instance=RequestContext(request))
