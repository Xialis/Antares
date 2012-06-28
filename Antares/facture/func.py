# -*- coding: utf-8 -*-
from facture.views import index, etapeInfo


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

    return ctrl(request)


def initCtrl(request):
    
    if not 'appFacture' in request.session:
        etapes = [[u"Recherche", index],
                   [u"Info client", etapeInfo],
                ]
        request.session['appFacture'] = {}
        request.session['appFacture']['etape'] = 0
        request.session['appFacture']['etapes'] = etapes
        
    return None


def ctrl(request):
    etapes = request.session['appFacture']['etapes']
    etape = request.session['appFacture']['etape']

    return etapes[etape][1]()
