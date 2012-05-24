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
    four = Fournisseur.objects.get(pk=fid)
    c['four'] = four
    formType = TypeForm().filtre_fournisseur(fid)
    c['formType'] = formType
    #Form Intitulés
    formTraitement = TraitementForm()
    formDiametre = DiametreForm()
    formCouleur = CouleurForm()
    
    #--
    
    if request.method == "POST":
        POST = request.POST
        
        if 'ajType'in POST:
            formType = TypeForm(POST)
        else:
            if 'ajTraitement' in POST:
                form = TraitementForm(POST)
            elif 'ajDiametre' in POST:
                form = DiametreForm(POST)
            elif 'ajCouleur' in POST:
                form = CouleurForm(POST)
                
            if form and form.is_valid():
                temp = form.save(commit=False)
                temp.fournisseur = Fournisseur.objects.get(id=fid)
                temp.save()
                
    #Context : Form Intitulé
    c['formTraitement'] = formTraitement
    c['listTraitement'] = Traitement.objects.filter(fournisseur__id=fid)
    c['formDiametre'] = formDiametre
    c['listDiametre'] = Diametre.objects.filter(fournisseur__id=fid)
    c['formCouleur'] = formCouleur
    c['listCouleur'] = Couleur.objects.filter(fournisseur__id=fid)
    # --
    
    c.update(csrf(request))
    return render_to_response('fournisseur/fournisseur.html', c)
