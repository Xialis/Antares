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

    c['listeClient'] = listeClient
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

    totalClients = Client.objects.all().count()
    listeClient = Client.objects.all()[debut:debut + taille]
    retour.update({"iTotalRecords": totalClients, "iTotalDisplayRecords": totalClients})
    aaData = []

    for client in listeClient:
        action = u"<a href='" + reverse(infoClient, args=[client.id]) + u"' class='action'>Détails</a>"
        aaData.append([client.code, client.nom + " " + client.prenom, client.telephone, client.email, action])

    retour.update({"aaData": aaData})
    return HttpResponse(simplejson.dumps(retour))
