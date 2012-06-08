# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib import messages
from django.core.context_processors import csrf
from django.db.utils import IntegrityError
from django.shortcuts import render_to_response, redirect

from fournisseur.models import Fournisseur
from stock.models import LigneStock
from stock.forms import AjoutForm, ModificationForm, RechercheForm


def index(request):
    c = {}
    listeFournisseur = Fournisseur.objects.all()

    c['listeFournisseur'] = listeFournisseur
    return render_to_response("stock/index.html", c)


def gestionStock(request, fid):
    c = {}
    fournisseur = Fournisseur.objects.get(id=fid)
    listeStock = LigneStock.objects.filter(fournisseur=fournisseur)

    formAjout = AjoutForm().filtre_fournisseur(fid).pasdechoix()
    formModification = ModificationForm(prefix='mod')
    formRecherche = RechercheForm().filtre_stock(fid)

    if request.method == 'POST':

        if 'ajout' in request.POST:
            formAjout = AjoutForm(request.POST).filtre_fournisseur(fid)
            if formAjout.is_valid():
                nouvligne = formAjout.save(commit=False)
                nouvligne.fournisseur = fournisseur
                nouvligne.save()
                messages.success(request, u"Verre ajouté avec succès !")
                formAjout = AjoutForm().filtre_fournisseur(fid)

    c['formAjout'] = formAjout
    c['formModification'] = formModification
    c['formRecherche'] = formRecherche
    c['listeStock'] = listeStock
    c['fournisseur'] = fournisseur
    c['messages'] = messages.get_messages(request)
    c.update(csrf(request))
    return render_to_response("stock/gestion.html", c)
