# -*- coding: utf-8 -*-
# Create your views here.
from fournisseur.models import *
from fournisseur.forms import *
from django.shortcuts import render_to_response
from django.core.context_processors import csrf


def index(request):
    c = {}
    formFour = FourForm()
    listFour = Fournisseur.objects.all()
    
    if request.method == 'POST':
        if 'nouvFour' in request.POST:
            formFour = FourForm(request.POST)
            if formFour.is_valid():
                formFour.save()
    
    c['formFour'] = formFour
    c['listFour'] = listFour
    c.update(csrf(request))
    return render_to_response('fournisseur/index.html', c)


def fournisseur(request, fid):
    c = {}
    FOUR = Fournisseur.objects.get(pk=fid)
    c['four'] = FOUR
    formType = TypeForm().filtre_fournisseur(fid)
    
    #Form Intitulés
    formTraitement = TraitementForm()
    formDiametre = DiametreForm()
    formCouleur = CouleurForm()

    #--

    if request.method == "POST":
        POST = request.POST

        if 'ajType' in POST:
            form = TypeForm(POST).filtre_fournisseur(fid)
            if form.is_valid():
                newtype = form.save(commit=False)
                newtype.fournisseur = FOUR
                newtype.save()
                form.save_m2m()
            else:
                formType = form

        else:
            if 'ajTraitement' in POST:
                form = TraitementForm(POST)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.fournisseur = FOUR
                    temp.save()
                else:
                    formTraitement = form

            elif 'ajDiametre' in POST:
                form = DiametreForm(POST)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.fournisseur = FOUR
                    temp.save()
                else:
                    formDiametre = form

            elif 'ajCouleur' in POST:
                form = CouleurForm(POST)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.fournisseur = FOUR
                    temp.save()
                else:
                    formCouleur = form

    #Context : Form Intitulé
    c['formTraitement'] = formTraitement
    c['listTraitement'] = Traitement.objects.filter(fournisseur__id=fid)
    c['formDiametre'] = formDiametre
    c['listDiametre'] = Diametre.objects.filter(fournisseur__id=fid)
    c['formCouleur'] = formCouleur
    c['listCouleur'] = Couleur.objects.filter(fournisseur__id=fid)
    # --
    #Context : Type
    c['formType'] = formType
    c['listType'] = Type.objects.filter(fournisseur__id=fid)
    #--
    c.update(csrf(request))
    return render_to_response('fournisseur/fournisseur.html', c)
