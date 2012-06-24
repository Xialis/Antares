# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson

from client.models import *
from client.forms import *
from client.func import ajoutClient, ajoutPrescripteur, ajoutOrganisme


def index(request):
    c = {}
    listeClient = Client.objects.all()

    formAjoutClient = FormAjoutClient()
    formAjoutOrganisme = FormAjoutOrganisme()
    formAjoutPrescripteur = FormAjoutPrescripteur()
    formRechercheClient = FormRechercheClient()

    b_listeFiltree = False
    if "appClient" in request.session:
        if "filtrage" in request.session["appClient"]:
            b_listeFiltree = True
            formRechercheClient = FormRechercheClient(request.session['appClient']['formRechercheClient'])
        else:
            request.session["appClient"] = {}
    else:
        request.session["appClient"] = {}

    if request.method == 'POST':

        if 'ajClient' in request.POST:
            retour = ajoutClient(FormAjoutClient(request.POST))
            listeClient = Client.objects.all()

            if retour['b_sauver'] == False:
                formAjoutClient = retour['form']

        if 'ajPrescripteur' in request.POST:
            retour = ajoutPrescripteur(FormAjoutPrescripteur(request.POST))

            if retour['b_sauver'] == False:
                formAjoutPrescripteur = retour['form']

        if 'ajOrganisme' in request.POST:
            retour = ajoutOrganisme(FormAjoutOrganisme(request.POST))

            if retour['b_sauver'] == False:
                formAjoutOrganisme = retour['form']

        if 'reClient' in request.POST:
            #reset
            if "filtrage" in request.session['appClient']:
                formRechercheClient = FormRechercheClient()
                del request.session['appClient']['filtrage']
                del request.session['appClient']['formRechercheClient']
            b_listeFiltree = False

            filtrage = Client.objects.all()
            form = FormRechercheClient(request.POST)
            if form.is_valid():
                cd = form.cleaned_data

                if cd.get("code"):
                    filtrage = filtrage.filter(code__contains=cd.get("code"))
                    b_listeFiltree = True

                if cd.get("nom"):
                    filtrage = filtrage.filter(nom__contains=cd.get("nom"))
                    b_listeFiltree = True

                if cd.get("prenom"):
                    filtrage = filtrage.filter(prenom__contains=cd.get("prenom"))
                    b_listeFiltree = True

                if cd.get("telephone"):
                    filtrage = filtrage.filter(telephone__contains=cd.get("telephone"))
                    b_listeFiltree = True

                if cd.get("email"):
                    filtrage = filtrage.filter(email__contains=cd.get("email"))
                    b_listeFiltree = True

                if cd.get("organisme"):
                    filtrage = filtrage.filter(organisme=cd.get("organisme"))
                    b_listeFiltree = True

                if b_listeFiltree == True:
                    formRechercheClient = FormRechercheClient(request.POST)
                    request.session["appClient"]["filtrage"] = filtrage
                    request.session['appClient']['formRechercheClient'] = request.POST

                else:
                    if "filtrage" in request.session['appClient']:
                        del request.session['appClient']['filtrage']
                        del request.session['appClient']['formRechercheClient']

    request.session.modified = True

    c['listeClient'] = listeClient
    c['listeFiltree'] = b_listeFiltree
    c['listeOrganisme'] = OrganismePayeur.objects.all()
    c['listePrescripteur'] = Prescripteur.objects.all()
    c['formAjoutClient'] = formAjoutClient
    c['formRechercheClient'] = formRechercheClient
    c['formAjoutOrganisme'] = formAjoutOrganisme
    c['formAjoutPrescripteur'] = formAjoutPrescripteur
    c.update(csrf(request))
    return render_to_response("client/index.html", c)


def infoClient(request, cid):
    c = {}

    return render_to_response("client/infoClient.html", c)


def ajaxListClient(request):
    retour = {}
    debut = 0
    taille = 10

    if request.GET.get("sEcho"):
        retour.update({"sEcho": request.GET.get("sEcho")})

    if request.GET.get("iDisplayStart"):
        debut = request.GET.get("iDisplayStart")

    if request.GET.get("iDisplayLength"):
        taille = request.GET.get("iDisplayLength")
        retour.update({"iDisplayLength": taille})

    listeClient = Client.objects.all()
    totalClients = listeClient.count()

    if "filtrage" in request.session["appClient"]:
        listeClient = request.session['appClient']['filtrage']
        totalClientsFiltre = listeClient.count()
    else:
        totalClientsFiltre = totalClients

    listeClient = listeClient.all()[debut:debut + taille]
    retour.update({"iTotalRecords": totalClients, "iTotalDisplayRecords": totalClientsFiltre})
    aaData = []

    for client in listeClient:
        action = u"<a href='" + reverse(infoClient, args=[client.id]) + u"' class='action'>Détails</a>"
        aaData.append([client.code, client.nom + " " + client.prenom, client.telephone, client.email, action])

    retour.update({"aaData": aaData})
    return HttpResponse(simplejson.dumps(retour))
