# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib import messages
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

from fournisseur.models import Fournisseur
from stock.models import LigneStock
from stock.forms import AjoutForm, ModificationForm, RechercheForm


def index(request):
    c = {}
    listeFournisseur = Fournisseur.objects.all()

    c['listeFournisseur'] = listeFournisseur
    c.update(csrf(request))
    return render_to_response("stock/index.html", c)


def gestionStock(request, fid):
    c = {}
    fournisseur = Fournisseur.objects.get(id=fid)
    listeStock = LigneStock.objects.filter(fournisseur=fournisseur)
    filtre = False

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

        if 'stockmod' in request.POST:
            formModification = ModificationForm(request.POST, prefix='mod')
            if formModification.is_valid():
                cd = formModification.cleaned_data
                ls = LigneStock.objects.get(id=cd['lid'])

                if cd['supprimer']:
                    ls.delete()
                else:
                    ls.quantite = cd['quantite']
                    ls.seuil = cd['seuil']
                    ls.save()

                listeStock = LigneStock.objects.filter(fournisseur=fournisseur)
                formModification = ModificationForm(prefix='mod')
                messages.success(request, u"Modification sauvée")

        if 'rechercher' in request.POST:
            formRecherche = RechercheForm(request.POST).filtre_stock(fid)
            if formRecherche.is_valid():
                cd = formRecherche.cleaned_data

                if cd['vtype'].__len__() != 0:
                    listeStock = listeStock.filter(vtype__in=cd['vtype'])
                    filtre = True

                if cd['diametre'].__len__() != 0:
                    listeStock = listeStock.filter(diametre__in=cd['diametre'])
                    filtre = True

                if cd['traitement'].__len__() != 0:
                    listeStock = listeStock.filter(traitement__in=cd['traitement'])
                    filtre = True

                if cd['couleur'].__len__() != 0:
                    listeStock = listeStock.filter(couleur__in=cd['couleur'])
                    filtre = True

                if cd['sphere'] is not None:
                    listeStock = listeStock.filter(sphere=cd['sphere'])
                    filtre = True

                if cd['cylindre'] is not None:
                    listeStock = listeStock.filter(cylindre=cd['cylindre'])
                    filtre = True

    c['filtre'] = filtre
    c['formAjout'] = formAjout
    c['formModification'] = formModification
    c['formRecherche'] = formRecherche
    c['listeStock'] = listeStock
    c['fournisseur'] = fournisseur
    c['messages'] = messages.get_messages(request)
    c.update(csrf(request))
    return render_to_response("stock/gestion.html", c)
