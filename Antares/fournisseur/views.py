# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib import messages
from django.core.context_processors import csrf
from django.db.utils import IntegrityError
from django.shortcuts import render_to_response, redirect
from fournisseur.forms import *
from fournisseur.models import *


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
                try:
                    newtype.save()
                except IntegrityError:
                    formType = form.erreurDuplica()
                    messages.error(request, "Oups, Erreur dans le formulaire d'ajout d'un nouveau Type")
                else:
                    form.save_m2m()
                    messages.success(request, u"Type ajouté avec succès !")
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
    c['messages'] = messages.get_messages(request)
    return render_to_response('fournisseur/fournisseur.html', c)


def modType(request, tid):
    c = {}

    t = Type.objects.get(id=tid)
    f = t.fournisseur

    formType = TypeForm(instance=t).filtre_fournisseur(f.id)

    if request.method == 'POST':
        formType = TypeForm(request.POST, instance=t).filtre_fournisseur(f.id)
        if formType.is_valid():
            try:
                formType.save()
            except IntegrityError:
                formType.erreurDuplica()
                messages.error(request, u"Oups, Erreur dans le formulaire")
            else:
                messages.success(request, u"Modification du Type: Type modifié avec succès")
                return redirect('fournisseur', fid=f.id)
        else:
            messages.error(request, u"Oups, Erreur dans le formulaire")

    c['four'] = f
    c['type'] = t
    c['formType'] = formType
    c.update(csrf(request))
    c['messages'] = messages.get_messages(request)
    return render_to_response('fournisseur/mod_Type.html', c)


def modTraitement(request, tid):
    obj = Traitement.objects.get(id=tid)
    c = {'objclass': obj.__class__.__name__, }
    f = obj.fournisseur
    
    form = TraitementForm(instance=obj)
    
    if request.method == "POST":
        form = TraitementForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                form.erreurDuplica()
                messages.error(request, u"Oups, Erreur dans le formulaire")
            else:
                messages.success(request, u"Modification du Traitement: Traitement modifié avec succès")
                return redirect('fournisseur', fid=f.id)
        else:
            messages.error(request, u"Oups, Erreur dans le formulaire")
    
    c['four'] = f
    c['form'] = form
    c.update(csrf(request))
    c['messages'] = messages.get_messages(request)
    return render_to_response('fournisseur/mod_generic.html', c)