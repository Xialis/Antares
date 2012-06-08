# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib import messages
from django.core.context_processors import csrf
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson

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


def modDiametre(request, did):
    obj = Diametre.objects.get(id=did)
    c = {'objclass': obj.__class__.__name__, }
    f = obj.fournisseur
    
    form = DiametreForm(instance=obj)
    
    if request.method == "POST":
        form = DiametreForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                form.erreurDuplica()
                messages.error(request, u"Oups, Erreur dans le formulaire")
            else:
                messages.success(request, u"Modification du Diametre: Diametre modifié avec succès")
                return redirect('fournisseur', fid=f.id)
        else:
            messages.error(request, u"Oups, Erreur dans le formulaire")
    
    c['four'] = f
    c['form'] = form
    c.update(csrf(request))
    c['messages'] = messages.get_messages(request)
    return render_to_response('fournisseur/mod_generic.html', c)


def modCouleur(request, cid):
    obj = Couleur.objects.get(id=cid)
    c = {'objclass': obj.__class__.__name__, }
    f = obj.fournisseur
    
    form = CouleurForm(instance=obj)
    
    if request.method == "POST":
        form = CouleurForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                form.erreurDuplica()
                messages.error(request, u"Oups, Erreur dans le formulaire")
            else:
                messages.success(request, u"Modification d'une Couleur: couleur modifiée avec succès")
                return redirect('fournisseur', fid=f.id)
        else:
            messages.error(request, u"Oups, Erreur dans le formulaire")
    
    c['four'] = f
    c['form'] = form
    c.update(csrf(request))
    c['messages'] = messages.get_messages(request)
    return render_to_response('fournisseur/mod_generic.html', c)


def ajax_filtre_traitement(request, qs=None):
    if qs is None:
        qs = []

    if request.GET.get('vtype'):
        qs = Traitement.objects.filter(type__pk=request.GET.get('vtype'))

    results = []
    for choice in qs:
        results.append((choice.pk, choice.nom))

    return HttpResponse(simplejson.dumps(results))


def ajax_filtre_diametre(request, qs=None):
    if qs is None:
        qs = Diametre.objects.all()

    if request.GET.get('vtype'):
        qs = qs.filter(type__pk=request.GET.get('vtype'))

    results = []
    for choice in qs:
        results.append((choice.pk, choice.nom))

    return HttpResponse(simplejson.dumps(results))


def ajax_filtre_couleur(request, qs=None):
    if qs is None:
        qs = Couleur.objects.all()

    if request.GET.get('vtype'):
        qs = qs.filter(type__pk=request.GET.get('vtype'))

    results = []
    for choice in qs:
        results.append((choice.pk, choice.nom))

    return HttpResponse(simplejson.dumps(results))
