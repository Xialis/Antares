# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from facture import views


def utiliserClient(request, cid):
    request.session['appFacture']['client_id'] = cid
    request.session['appFacture']['etape'] = 1
    request.session.modified = True
    return redirect(ctrl)


def creerClient(request):
    if 'appFacture' in request.session:
        del request.session['appFacture']
        initCtrl(request)

    request.session['appFacture']['etape'] = 1
    request.session.modified = True
    return redirect(ctrl)


def enrClient(request):
    if request.method == 'POST':
        request.session['appFacture']['post_infoClient'] = request.POST
        request.session.modified = True
        return True

    return False


def effClient(request):
    if 'post_infoClient' in request.session['appFacture']:
        del request.session['appFacture']['post_infoClient']
        request.session.modified = True
        return True
    
    return False


def etapePrecedente(request):
    request.session['appFacture']['etape'] -= 1
    request.session.modified = True
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

    return redirect(ctrl)


def creationClient(b_creation, request):
    request.session['appFacture']['b_creation'] = b_creation
    request.session.modified = True
    return b_creation


def initCtrl(request):

    if not 'appFacture' in request.session:
        etapes = [[u"Recherche", views.etapeRecherche],
                   [u"Info client", views.etapeInfo],
                   [u"Prescription", views.etapePrescription],
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