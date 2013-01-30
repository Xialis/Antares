# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from client.models import *
from client.forms import *
from client.func import ajoutClient, ajoutPrescripteur, ajoutOrganisme, filtration, initFiltration

from facture.models import Facture
import facture.func


@login_required
def index(request):
    c = {}
    listeClient = Client.objects.all()

    formAjoutClient = FormAjoutClient()
    formAjoutOrganisme = FormAjoutOrganisme()
    formAjoutPrescripteur = FormAjoutPrescripteur()
    formRechercheClient = FormRechercheClient()

    riF = initFiltration(request)
    if riF['b_listeFiltree']:
        b_listeFiltree = True
        formRechercheClient = FormRechercheClient(riF['posted'])
    else:
        b_listeFiltree = False

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

            retour = filtration(request)
            b_listeFiltree = retour['b_listeFiltree']
            if b_listeFiltree == True:
                formRechercheClient = FormRechercheClient(request.POST)
            else:
                formRechercheClient = FormRechercheClient()

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


@login_required
def infoClient(request, cid):
    c = {}
    client = Client.objects.get(id=cid)
    c['client'] = client
    c['proformas'] = Facture.objects.filter(client=client, bproforma=True).order_by('-date_modification')
    c['factures'] = Facture.objects.filter(client=client, bproforma=False).order_by('-date_modification')
    c['prescriptions'] = Prescription.objects.filter(client=client)

    if request.GET.get('fiddownload'):
        c['fiddownload'] = request.GET.get('fiddownload')

    if request.method == 'GET':

        # Facturer directement
        if request.GET.get("mode", False) == 'direct':
            fac = facture.func.facturer(request.GET.get("pfid"))
            if fac is None:
                messages.error(request, u"Erreur de transformation")
            elif fac == -1:
                messages.error(request, u"Cette proforma est déjà facturée")
            else:
                messages.success(request, "La facture " + fac.numero + " a été créée")

            return redirect(request.path)

    return render_to_response("client/infoClient.html", c, context_instance=RequestContext(request))


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
        action = u"<a href='" + reverse(infoClient, args=[client.id]) + u"' class='l-button ui-state-default ui-corner-all'><span class='ui-icon ui-icon-folder-open'></span>Détails</a>"
        action += u" <a href='" + reverse(facture.func.utiliserClient, args=[client.id]) + u"' class='l-button ui-state-default ui-corner-all'><span class='ui-icon ui-icon-person'></span>Utiliser</a>"
        aaData.append([client.code, client.nom + " " + client.prenom, client.telephone, client.email, action])

    retour.update({"aaData": aaData})
    return HttpResponse(simplejson.dumps(retour))
