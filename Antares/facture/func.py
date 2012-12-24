# -*- coding: utf-8 -*-
from datetime import date
from django.shortcuts import redirect

from facture.views import etapeRecherche, etapeInfo, etapePrescription, etapeMontures, etapeVerres, etapeOptions, etapeRecapitulatif
from facture.models import Facture
from Antares.Verrou import Verrou


#===============================================================================
# gestion Client
#===============================================================================
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
        request.session['appFacture']['prescription_t'] = prescription.transposition()

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
    raise DeprecationWarning("Utiliser la fonction de la class Prescription !")


def getSphereCylNeg(sphere, cylindre):
    ns = sphere

    if cylindre > 0:
        # x = sph + cyl
        # -cyl + x = sph
        ns = sphere - cylindre

    return ns


#===============================================================================
# gestion Verres
#===============================================================================
def enrVerres(formsets, request):
    u"""Enregistre les verres dans la session

    Arguments:
    formsets -- cf. facture.views.etapeVerres pour le format
    request -- la requete en cours (accès à la session)

    """
    t = []
    for x in xrange(0, len(formsets)):  # nombre d'ensemble (monture)
        monture = formsets[x]["monture"]
        formset = formsets[x]["formset"]
        tm = []

        lfd = formset[0].save(commit=False)
        lfd.oeil = 'D'
        lfd.monture = monture.numero
        lfd.tarif = lfd.calculTotal()
        lfd.remise_monture = lfd.calculRemise()

        if len(formset[1].cleaned_data) != 0:
            # on a un OG
            lfg = formset[1].save(commit=False)
            lfg.oeil = 'G'
            lfg.monture = monture.numero
            lfg.tarif = lfg.calculTotal()
            lfg.remise_monture = lfg.calculRemise()
            tm.append(lfd)
            tm.append(lfg)
        else:
            # les deux yeux d'un coup ?
            # voir monture.oeil
            if monture.oeil == 'T':
                lfd.oeil = 'T'
                lfd.tarif *= 2
                lfd.remise_monture *= 2
            else:
                lfd.oeil = monture.oeil

            tm.append(lfd)

        t.append(tm)

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
