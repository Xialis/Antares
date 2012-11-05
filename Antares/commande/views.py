# -*- coding: utf-8 -*-

# import Django
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.db.models import F

# import Antares
from fournisseur.models import Fournisseur
from commande.models import Commande, LigneCommande
from stock.models import LigneStock
import func


def index(request):
    c = {}

    listeFournisseur = Fournisseur.objects.all()

    c['listeFournisseur'] = listeFournisseur
    c.update(csrf(request))
    return render_to_response("commande/index.html", c, context_instance=RequestContext(request))


def commandesF(request, fid):
    c = {}
    listeCommandes = Commande.objects.filter(fournisseur__id=fid).order_by('-id')
    cid = listeCommandes[0].id

    # gestion commande stock
    liste = []
    listeStock = LigneStock.objects.filter(fournisseur__id=fid).filter(quantite__lt=F('seuil'))

    for ligne in listeStock:
        diff = ligne.seuil - ligne.quantite
        qtcom = 0  # Quantité déjà commandée
        for lc in LigneCommande.objects.filter(ligne_stock=ligne, quantite__lt=F('quantite_recu')):
            qtcom = qtcom + lc.quantite - lc.quantite_recu

        if diff > qtcom:
            qtacom = diff - qtcom
            liste.append({'lignestock': ligne, 'qtcom': qtcom, 'qtacom': qtacom})
    
    c['liste'] = liste
    c['listeStock'] = listeStock
    c['listeCommandes'] = listeCommandes
    c['cid'] = cid
    c.update(csrf(request))
    return render_to_response("commande/commandesF.html", c, context_instance=RequestContext(request))


def validationCommande(request, cid):
    commande = Commande.objects.get(id=cid)
    if func.validerCommande(commande):
        messages.success(request, u"Commande validée")
        func.nouvelleCommande(commande.fournisseur)
    else:
        messages.error(request, u"Erreur de validation")

    return redirect(commandesF, fid=commande.fournisseur)
