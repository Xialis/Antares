# -*- coding: utf-8 -*-

# import Django
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory

# import Antares
from fournisseur.models import Fournisseur
from commande.models import Commande
import func


def index(request):
    c = {}

    listeFournisseur = Fournisseur.objects.all()

    c['listeFournisseur'] = listeFournisseur
    c.update(csrf(request))
    return render_to_response("commande/index.html", c, context_instance=RequestContext(request))


def commandesF(request, fid):
    c = {}
    fournisseur = Fournisseur.objects.get(id=fid)
    listeCommandes = Commande.objects.filter(fournisseur=fournisseur).order_by('-id')
    cid = listeCommandes[0].id

    # gestion commande stock
    liste = func.listeStock(fournisseur)

    c['liste'] = liste
    c['listeCommandes'] = listeCommandes
    c['cid'] = cid
    c.update(csrf(request))
    return render_to_response("commande/commandesF.html", c, context_instance=RequestContext(request))


def validationCommande(request, cid):
    commande = Commande.objects.get(id=cid)
    if func.validerCommande(commande):
        messages.add_message(request, messages.SUCCESS, u"Commande validée")
        func.nouvelleCommande(commande.fournisseur)
    else:
        messages.add_message(request, messages.ERROR, u"Erreur de validation, rien à commander !")

    return redirect(commandesF, fid=commande.fournisseur.id)
