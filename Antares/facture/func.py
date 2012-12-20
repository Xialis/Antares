# -*- coding: utf-8 -*-
from datetime import date
from django.shortcuts import redirect
from facture.views import *
from facture.models import LigneFacture, Monture, Option, Facture
from facture.forms import LigneForm
from Antares.Verrou import Verrou


def utiliserClient(request, cid):
    request.session['appFacture']['client_id'] = cid
    request.session['appFacture']['etape'] = 1
    request.session.modified = True
    return redirect(ctrl)


def creationClient(b_creation, request):
    request.session['appFacture']['b_creation'] = b_creation
    request.session.modified = True
    return b_creation


def modificationClient(b_modification, request):
    request.session['appFacture']['b_modification'] = b_modification
    request.session.modified = True
    return b_modification


def creerClient(request):
    if 'appFacture' in request.session:
        del request.session['appFacture']
        initCtrl(request)

    request.session['appFacture']['etape'] = 1
    request.session.modified = True
    return redirect(ctrl)


def enrClient(client, request):
    if request.method == 'POST':
        request.session['appFacture']['client'] = client
        request.session.modified = True
        return True

    return False


def effClient(request):
    if 'client' in request.session['appFacture']:
        del request.session['appFacture']['client']
        request.session.modified = True
        return True

    return False


def getClient(request):
    retour = {'client_id': None, 'client': None}
    if 'client' in request.session['appFacture']:
        retour['client'] = request.session['appFacture']['client']

    if 'client_id' in request.session['appFacture']:
        retour['client_id'] = request.session['appFacture']['client_id']

    return retour


def enrPrescription(prescription, request):
    if request.method == 'POST':
        request.session['appFacture']['prescription'] = prescription

        if prescription.addition_od != 0 and prescription.addition_od is not None:
            request.session['appFacture']['progressif_od'] = True
        else:
            request.session['appFacture']['progressif_od'] = False

        if prescription.addition_og != 0 and prescription.addition_og is not None:
            request.session['appFacture']['progressif_og'] = True
        else:
            request.session['appFacture']['progressif_og'] = False

        # Transposition
        request.session['appFacture']['prescription_t'] = transposition(prescription)

        # Sphere en cylindre moins (test vision)
        request.session['appFacture']['prescription_sphod'] = getSphereCylNeg(prescription.sphere_od, prescription.cylindre_od)
        request.session['appFacture']['prescription_sphog'] = getSphereCylNeg(prescription.sphere_og, prescription.cylindre_og)

        request.session.modified = True
        return True

    return False


def getPrescription(request):
    if 'prescription' in request.session['appFacture']:
        return request.session['appFacture']['prescription']

    return None


def getPrescription_T(request):
    if 'prescription_t' in request.session['appFacture']:
        return request.session['appFacture']['prescription_t']

    return None


def transposition(prescription):
    # TODO: Remplacer par la fonction de class !
    ptrans = Prescription()

    # nouvelle sphere = sphere + cylindre-negatif
    # nouveau cylindre = cylindre-negatif * -1
    # nouvel axe = (axe + 90) % 180 (0<=axe<=179)
    if prescription.cylindre_od and prescription.cylindre_od < 0:
        ptrans.sphere_od = prescription.sphere_od + prescription.cylindre_od
        ptrans.cylindre_od = abs(prescription.cylindre_od)
        ptrans.axe_od = (prescription.axe_od + 90) % 180
    else:
        ptrans.sphere_od = prescription.sphere_od
        ptrans.cylindre_od = prescription.cylindre_od
        ptrans.axe_od = prescription.axe_od

    if prescription.cylindre_og and prescription.cylindre_og < 0:
        ptrans.sphere_og = prescription.sphere_og + prescription.cylindre_og
        ptrans.cylindre_og = abs(prescription.cylindre_og)
        ptrans.axe_og = (prescription.axe_og + 90) % 180
    else:
        ptrans.sphere_og = prescription.sphere_og
        ptrans.cylindre_og = prescription.cylindre_og
        ptrans.axe_og = prescription.axe_og

    ptrans.addition_od = prescription.addition_od
    ptrans.addition_og = prescription.addition_og

    return ptrans


def getSphereCylNeg(sphere, cylindre):
    ns = sphere

    if cylindre > 0:
        # x = sph + cyl
        # -cyl + x = sph
        ns = sphere - cylindre

    return ns


def enrVerres(formSetLigne, request):
    t = []
    nbre = len(formSetLigne.cleaned_data)
    nloop = nbre / 2
    for x in range(0, nloop):
        start = x * 2
        if len(formSetLigne[start].cleaned_data) != 0:
            lfd = formSetLigne[start].save(commit=False)
            lfd.oeil = 'D'
            lfd.monture = x

            # tarif: tarif_type + tarif_couleur + tarif_traitement
            tarif_type = lfd.vtype.tarif
            tarif_couleur = lfd.couleur.tarif
            tarif_traitement = lfd.traitement.tarif
            lfd.tarif = tarif_type + tarif_couleur + tarif_traitement

            if len(formSetLigne[start + 1].cleaned_data) != 0:
                lfg = formSetLigne[start + 1].save(commit=False)
                lfg.oeil = 'G'
                lfg.monture = x
                tarif_type = lfg.vtype.tarif
                tarif_couleur = lfg.couleur.tarif
                tarif_traitement = lfg.traitement.tarif
                lfg.tarif = tarif_type + tarif_couleur + tarif_traitement
                t.append(lfd)
                t.append(lfg)
            else:
                lfd.oeil = 'T'
                lfd.tarif = lfd.tarif * 2
                t.append(lfd)

    request.session['appFacture']['LigneFacture'] = t
    request.session['appFacture']['etapeVerres_post'] = request.POST
    request.session.modified = True
    return request


def getVerres(request):
    if 'LigneFacture' in request.session['appFacture']:
        return request.session['appFacture']['LigneFacture']

    return []


def getNbreMontures(request):
    t = request.session['appFacture']['Montures']
    taille = len(t)
    return taille


def enrMontures(formSetMonture, request):
    t = []
    x = 0
    for f in formSetMonture:
        nom = f.cleaned_data.get('nom')
        tarif = f.cleaned_data.get('tarif')

        if nom is None and tarif is None:
            pass
        else:
            monture = f.save(commit=False)
            monture.numero = x
            x += 1
            t.append(monture)

    request.session['appFacture']['Montures'] = t
    request.session['appFacture']['etapeMontures_post'] = request.POST
    request.session.modified = True
    return True


def getMontures(request):
    if 'Montures' in request.session['appFacture']:
        return request.session['appFacture']['Montures']


def enrOptions(formSetOption, request):
    t = []

    for f in formSetOption:
        if f.is_valid():
            if f.cleaned_data.get('nom') and f.cleaned_data['nom'] != '':
                option = f.save(commit=False)
                t.append(option)

    request.session['appFacture']['Options'] = t
    request.session['appFacture']['etapeOptions_post'] = request.POST
    request.session.modified = True
    return True


def getOptions(request):
    if 'Options' in request.session['appFacture']:
        return request.session['appFacture']['Options']


def etapePrecedente(request):
    request.session['appFacture']['etape'] -= 1
    request.session.modified = True
    if request.session['appFacture']['etape'] < 0:
        request.session['appFacture']['etape'] = 0
    return redirect(ctrl)


def etapeSuivante(request):
    request.session['appFacture']['etape'] += 1
    request.session.modified = True
    return redirect(ctrl)


def allerEtape(request, etape):
    return None


def reset(request):
    if 'appFacture' in request.session:
        del request.session['appFacture']
        request.session.modified = True
    return redirect(ctrl)


def initCtrl(request):

    if not 'appFacture' in request.session:
        etapes = [[u"Recherche", etapeRecherche],
                   [u"Info client", etapeInfo],
                   [u"Prescription", etapePrescription],
                   [u"Montures", etapeMontures],
                   [u"Verres", etapeVerres],
                   [u"Options", etapeOptions],
                   [u"Recapitulatif", etapeRecapitulatif]
                ]
        request.session['appFacture'] = {}
        request.session['appFacture']['etape'] = 0
        request.session['appFacture']['etapes'] = etapes
        creationClient(True, request)
        request.session.modified = True
    return None


def ctrl(request):

    initCtrl(request)

    etapes = request.session['appFacture']['etapes']
    etape = request.session['appFacture']['etape']

    return etapes[etape][1](request)


def sauvFacture(facture):

    verrou = Verrou('codeFacture.lock')

    if facture.bproforma == True:
        lettre = 'P'
    else:
        lettre = 'F'

    while verrou.ferme() == 0:
        pass

    dj = date.today()
    debut_code = dj.strftime("%Y") + dj.strftime("%m") + dj.strftime("%d")
    compteur = Facture.objects.filter(numero__startswith=debut_code).count()
    if compteur < 10:
        s_compteur = '00' + str(compteur + 1)
    elif compteur < 100:
        s_compteur = '0' + str(compteur + 1)

    code = debut_code + s_compteur + lettre
    facture.numero = code
    facture.save()

    verrou.ouvre()

    return facture
