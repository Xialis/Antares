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
        
        if 'ajTraitement' in POST:
            formTraitement = TraitementForm(POST)
            if formTraitement.is_valid():
                traitement = formTraitement.save(commit=False)
                traitement.fournisseur = Fournisseur.objects.get(id=fid)
                traitement.save()
                
    #Context : Form Intitulé
    c['formTraitement'] = formTraitement
    c['listTraitement'] = Traitement.objects.filter(fournisseur__id=fid)
    c['formDiametre'] = formDiametre
    c['formCouleur'] = formCouleur
    # --
    
    c.update(csrf(request))
    return render_to_response('fournisseur/fournisseur.html', c)
