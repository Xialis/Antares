# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from facture import views


def utiliserClient(request, cid):
    return None


def creerClient(request):
    return None


def etapePrecedente(request):
    return None


def etapeSuivante(request):
    return None


def allerEtape(request, etape):
    return None


def reset(request):
    if 'appFacture' in request.session:
        del request.session['appFacture']

    return redirect(ctrl)


def initCtrl(request):

    if not 'appFacture' in request.session:
        etapes = [[u"Recherche", views.etapeRecherche],
                   [u"Info client", views.etapeInfo],
                ]
        request.session['appFacture'] = {}
        request.session['appFacture']['etape'] = 0
        request.session['appFacture']['etapes'] = etapes
        request.session.modified = True
    return None


def ctrl(request):
    
    initCtrl(request)
    
    etapes = request.session['appFacture']['etapes']
    etape = request.session['appFacture']['etape']

    return etapes[etape][1](request)
