# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.functional import curry
from django.contrib.auth.decorators import login_required

from client.models import Client, Prescription
from client.forms import FormRechercheClient, FormAjoutClient, FormAjoutPrescription, FormAjoutPrescripteur

#from client.func import initFiltration, filtration, sauvClient
import client.func as cfunc

from fournisseur.models import Type, Diametre, Traitement, Couleur
import fournisseur.func as fourfunc

from stock.models import LigneStock

import func
from models import Facture, Interlocuteur
from facture.forms import LigneForm, MontureForm, OptionForm, ChoixFactureForm, SolderFactureForm, AjoutInterlocuteurForm


@login_required
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

    if request.GET.get('fiddownload'):
        c['fiddownload'] = request.GET.get('fiddownload')

    c.update(csrf(request))
    return render_to_response("facture/etapeRecherche.html", c, context_instance=RequestContext(request))


@login_required
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


@login_required
def etapePrescription(request):
    c = {}
    formPrescription = FormAjoutPrescription()
    formAjoutPrescripteur = FormAjoutPrescripteur(prefix="ajPrescripteur")
    if 'client_id' in request.session['appFacture']:
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


@login_required
def etapeVerres(request):
    c = {}
    montures = func.getMontures(request)
    formsets = []
    for m in montures:
        if m.vision == 'M':
            progressif = True
        else:
            progressif = False

        extra = 2  # ODG
        LigneFormSet = formset_factory(LigneForm, extra=extra)
        LigneFormSet.form = staticmethod(curry(LigneForm, progressif=progressif))
        formSetLigne = LigneFormSet(prefix=str(m.numero))
        formSetLigne.forms[0].empty_permitted = False
        formsets.append({"monture": m, "formset": formSetLigne})

    # ============================
    # Restauration / chargement à partir de la session
    if request.method == 'GET' and 'appFacture' in request.session:
        verres = func.getVerres(request)
        if len(verres) != 0:
            if len(verres) != len(montures):
                c['restauration_erreur'] = 1
            else:
                formsets = []
                for m in montures:
                    if m.numero < len(verres):
                        if m.vision == 'M':
                            progressif = True
                        else:
                            progressif = False

                        if len(verres[m.numero]) == 2:
                            if progressif != any(verres[m.numero][0].vtype.progressif, verres[m.numero][1].vtype.progressif):
                                c['restauration_erreur'] = 2
                        else:
                            if progressif != verres[m.numero][0].vtype.progressif:
                                c['restauration_erreur'] = 2
                                LigneFormSet.form = staticmethod(curry(LigneForm, progressif=progressif))
                                formSetLigne = LigneFormSet(prefix=str(m.numero))
                                formSetLigne.forms[0].empty_permitted = False
                                for form in formSetLigne:
                                    chdata = form._get_changed_data()
                                    if 'vtype' in chdata:
                                        form.filtre_vtype(form._raw_value('vtype'))

                                formsets.append({"monture": m, "formset": formSetLigne})
                            else:
                                prefix = str(m.numero)
                                data = {
                                        prefix + '-TOTAL_FORMS': u'2',
                                        prefix + '-INITIAL_FORMS': u'0',
                                        prefix + '-MAX_NUM_FORMS': u'',
                                        prefix + '-0-vtype': verres[m.numero][0].vtype,
                                        prefix + '-0-diametre': verres[m.numero][0].diametre,
                                        prefix + '-0-couleur': verres[m.numero][0].couleur,
                                        prefix + '-0-traitement': verres[m.numero][0].traitement,
                                        }

                                if len(verres[m.numero]) == 2:
                                    dataG = {
                                             prefix + '-1-vtype': verres[m.numero][1].vtype,
                                             prefix + '-1-diametre': verres[m.numero][1].diametre,
                                             prefix + '-1-couleur': verres[m.numero][1].couleur,
                                             prefix + '-1-traitement': verres[m.numero][1].traitement,
                                             }
                                    data.update(dataG)

                                LigneFormSet.form = staticmethod(curry(LigneForm, progressif=progressif))
                                formSetLigne = LigneFormSet(data, prefix=str(m.numero))
                                formSetLigne.forms[0].empty_permitted = False
                                for form in formSetLigne:
                                    chdata = form._get_changed_data()
                                    if 'vtype' in chdata:
                                        form.filtre_vtype(form._raw_value('vtype'))

                                formsets.append({"monture": m, "formset": formSetLigne})

    # Fin restauration
    # ============================

    if request.method == 'POST':

        if 'ajVerres' in request.POST:
            formsets = []
            valide = True
            for m in montures:
                if m.vision == 'M':
                    progressif = True
                else:
                    progressif = False

                extra = 2
                LigneFormSet = formset_factory(LigneForm, extra=extra)
                LigneFormSet.form = staticmethod(curry(LigneForm, progressif=progressif))
                formSetLigne = LigneFormSet(request.POST, prefix=str(m.numero))
                formSetLigne.forms[0].empty_permitted = False

                # On charge les choix disponibles pour validation...
                for form in formSetLigne:
                    chdata = form._get_changed_data()
                    if 'vtype' in chdata:
                        vtype = Type.objects.get(id=form._raw_value('vtype'))
                        form.filtre_vtype(vtype)

                if formSetLigne.is_valid():
                    valide = valide and True
                else:
                    valide = False

                formsets.append({"monture": m, "formset": formSetLigne})

            # -endfor

            if valide == True:
                func.enrVerres(formsets, request)
                return func.etapeSuivante(request)
            else:
                formsets = []
                for m in montures:
                    if m.vision == 'M':
                        progressif = True
                    else:
                        progressif = False

                    extra = 2
                    LigneFormSet = formset_factory(LigneForm, extra=extra)
                    LigneFormSet.form = staticmethod(curry(LigneForm, progressif=progressif))
                    formSetLigne = LigneFormSet(request.POST, prefix=str(m.numero))  # Si on ne refait pas un formset, le is_valid casse tout...
                    formSetLigne.forms[0].empty_permitted = False
                    for form in formSetLigne:
                        chdata = form._get_changed_data()
                        if 'vtype' in chdata:
                            vtype = Type.objects.get(id=form._raw_value('vtype'))
                            form.filtre_vtype(vtype)

                    formsets.append({"monture": m, "formset": formSetLigne})

        # -endif ajVerres
    # -endif POST

    c['formsets'] = formsets
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


#===============================================================================
# Etape Montures
#===============================================================================
@login_required
def etapeMontures(request):
    c = {}
    EXTRA = 3
    restauration = None
    MontureFormSet = formset_factory(MontureForm, extra=EXTRA)
    formSetMonture = MontureFormSet()
    for form in formSetMonture:
        form.empty_permitted = True
        if request.session['appFacture']['progressif_og'] or request.session['appFacture']['progressif_od']:
            pass
        else:
            form.choixvpvl()
    formSetMonture[0].empty_permitted = False

    # ============================
    # Restauration
    if request.method == 'GET' and 'Montures' in request.session['appFacture']:

        ms = func.getMontures(request)
        data = []
        for m in ms:
            data.append(m.__dict__)

        MontureFormSet = formset_factory(MontureForm, extra=EXTRA - len(data))
        formSetMonture = MontureFormSet(initial=data)
        for form in formSetMonture:
            form.empty_permitted = True
        formSetMonture[0].empty_permitted = False
        restauration = len(data)
    # Fin restauration
    # ============================

    # ============================
    # Traitement POST
    if request.method == 'POST':

        if 'ajMontures' in request.POST:
            formSetMonture = MontureFormSet(request.POST)
            for f in formSetMonture:
                f.empty_permitted = True
            formSetMonture[0].empty_permitted = False

            if formSetMonture.is_valid():
                func.enrMontures(formSetMonture, request)
                return func.etapeSuivante(request)

    # Fin POST
    # ============================

    c['formSetMonture'] = formSetMonture
    c['restauration'] = restauration
    c.update(csrf(request))
    return render_to_response("facture/etapeMontures.html", c, context_instance=RequestContext(request))


# ==
# Etape Options
#
@login_required
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
@login_required
def etapeRecapitulatif(request):
    c = {}
    s_aF = request.session['appFacture']
    formFacture = ChoixFactureForm()
    dico_client = func.getClient(request)
    client_orig = None
    solde = 0
    remise = 0

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

    # ======================
    # calcul du solde et remise
    ra = 0
    t_remise = [0, 0, 0]
    t_monturetarif = [0, 0, 0]

    for grp in t_verres:
        for v in grp:
            solde += v.tarif
            remise += v.calculRemise()
            t_remise[v.monture] += v.calculRemise()

    for o in t_options:
        solde += o.tarif

    for m in t_montures:
        solde += m.tarif
        t_monturetarif[m.numero] += m.tarif

    for m in range(0, len(t_remise)):
        if t_monturetarif[m] >= t_remise[m]:
            ra += t_remise[m]
        elif t_monturetarif[m] < t_remise[m]:
            ra += t_monturetarif[m]

    # ======================
    # traitment POST
    if request.method == 'POST':
        '''
        Enregistrement du client (s'il n'existe pas)
        ou Enregistrement des modifications (s'il y en a)
        Enregistrement de la prescrition
        Enregistrement de la Facture (génération ID)

        Enregistrement LigneFacture (verres)
        Si stock : traitement / Si "à commander" traitement.

        Enregistrement Monture(s)
        Enregistrement Options

        Reset assistant
        '''
        # Traitement Facture (-> facture.id)
        formFacture = ChoixFactureForm(request.POST)
        if formFacture.is_valid():
            facture = formFacture.save(commit=False)
            cd = formFacture.cleaned_data

            # Traitement client (-> client.id)
            if s_aF['b_creation'] == True:
                client = func.getClient(request)['client']
                client = cfunc.sauvClient(client)
            elif 'b_modification' in s_aF and s_aF['b_modification'] == True:
                client = func.getClient(request)['client']
                client_orig = Client.objects.get(id=dico_client['client_id'])

                client_orig.nom = client.nom
                client_orig.prenom = client.prenom
                client_orig.telephone = client.telephone
                client_orig.email = client.email
                client = client_orig.save()
            else:
                client = Client.objects.get(id=dico_client['client_id'])

            facture.client = client

            # Traitement de la prescription
            prescription = func.getPrescription(request)
            prescription.client = client
            prescription.save()

            facture.prescription = prescription

            # enregistrement de la facture
            facture = func.sauvFacture(facture)
            request.session['appFacture']['fid'] = facture.id

            # Traitement LigneFacture
            t_lignes = func.getVerres(request)
            for grp in t_lignes:
                for ligne in grp:
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

            #actualisation du solde
            if cd['avance'] is not None:
                facture.solde = facture.total() - cd['avance']
            else:
                facture.solde = facture.total()

            facture.save()

            # Si facture: Actualisation Commande ou Stock
            if not facture.bproforma:
                fourfunc.stock_ou_commande(facture.lignefacture_set.all())

            return func.etapeSuivante(request)

    c['client'] = client
    c['client_orig'] = client_orig
    c['t_verres'] = t_verres
    c['t_options'] = t_options
    c['t_montures'] = t_montures
    c['prescription'] = prescription
    c['prescription_t'] = prescription_t
    c['formFacture'] = formFacture
    c['soldeinitial'] = solde
    c['solde'] = solde - ra
    c['remise_max'] = remise
    c['remise_accordee'] = ra
    c.update(csrf(request))
    return render_to_response("facture/etapeRecapitulatif.html", c, context_instance=RequestContext(request))


@login_required
def etapeFinale(request):
    c = {}
    c['fiddownload'] = request.session['appFacture']['fid']
    func.reset(request)
    return render_to_response("facture/etapeFinale.html", c, context_instance=RequestContext(request))


#===============================================================================
# Voir facture non soldées
#===============================================================================
@login_required
def facnonsoldee(request):
    c = {}
    facs = Facture.objects.exclude(bproforma=True).exclude(solde=0)
    formSolder = SolderFactureForm()

    if request.method == "POST":

        formSolder = SolderFactureForm(request.POST)
        if formSolder.is_valid():
            cd = formSolder.cleaned_data
            fac = Facture.objects.get(id=cd['fid'])
            if fac.solde <= cd['remis']:
                fac.solde = 0
                fac.save()
                messages.success(request, "La facture %s a été soldée !", fac.numero)
                messages.info(request, "A rendre: %d", cd['remis'] - fac.solde)
            else:
                fac.solde = fac.solde - cd['remis']
                fac.save()
                messages.warning(request, "La facture %s n'est pas encore soldée", fac.numero)
                messages.info(request, "Reste à percevoir: %d", fac.solde - cd['remis'])

    c['facs'] = facs
    c['formSolder'] = formSolder
    c.update(csrf(request))
    return render_to_response("facture/facnonsoldee.html", c, context_instance=RequestContext(request))


#===============================================================================
# Parametres
#===============================================================================
@login_required
def parametres(request):
    c = {}
    interlocuteurs = Interlocuteur.objects.all()
    formAjoutInterlocuteur = AjoutInterlocuteurForm()

    if request.method == "POST":

        if "AjInterlocuteur" in request.POST:
            form = AjoutInterlocuteurForm(request.POST)
            if form.is_valid():
                form.save()
                nom = form.cleaned_data['nom']
                messages.info(request, u"Interlocuteur " + nom + u" ajouté")
            else:
                messages.error(request, "Erreur dans le formulaire")

        if "ModInterlocuteur" in request.POST:
            form = AjoutInterlocuteurForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                i = Interlocuteur.objects.get(id=cd['iid'])
                i.nom = cd['nom']
                i.save()
                messages.info(request, u"Interlocuteur " + i.nom + u" modifié")
            else:
                messages.error(request, "Erreur dans le formulaire de modification")

    c['interlocuteurs'] = interlocuteurs
    c['formAjoutInterlocuteur'] = formAjoutInterlocuteur
    c.update(csrf(request))
    return render_to_response("facture/parametres.html", c, context_instance=RequestContext(request))
