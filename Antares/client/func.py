# -*- coding: utf-8 -*-
from datetime import date
from client.models import Client
from client.forms import FormRechercheClient

from Antares.Verrou import Verrou


def ajoutClient(formAjoutClient):

    b_sauver = False
    dj = date.today()

    if formAjoutClient.is_valid():
        client = formAjoutClient.save(commit=False)
        #code
        debut_code = dj.strftime("%Y") + dj.strftime("%m") + dj.strftime("%d")
        compteur = Client.objects.filter(code__startswith=debut_code).count()
        if compteur < 10:
            s_compteur = '00' + str(compteur + 1)
        elif compteur < 100:
            s_compteur = '0' + str(compteur + 1)

        code = debut_code + s_compteur
        client.code = code
        client.save()
        b_sauver = True

    return {"form": formAjoutClient, "b_sauver": b_sauver}


def sauvClient(client):
    verrou = Verrou('codeClient.lock')
    while verrou.ferme() == 0:
        pass

    dj = date.today()
    debut_code = dj.strftime("%Y") + dj.strftime("%m") + dj.strftime("%d")
    compteur = Client.objects.filter(code__startswith=debut_code).count()
    if compteur < 10:
        s_compteur = '00' + str(compteur + 1)
    elif compteur < 100:
        s_compteur = '0' + str(compteur + 1)

    code = debut_code + s_compteur
    client.code = code
    client.save()

    verrou.ouvre()

    return client


def ajoutPrescripteur(formAjoutPrescripteur):

    b_sauver = False

    if formAjoutPrescripteur.is_valid():
        formAjoutPrescripteur.save()
        b_sauver = True

    return {"form": formAjoutPrescripteur, "b_sauver": b_sauver}


def ajoutOrganisme(formAjoutOrganisme):

    b_sauver = False

    if formAjoutOrganisme.is_valid():
        formAjoutOrganisme.save()
        b_sauver = True

    return {"form": formAjoutOrganisme, "b_sauver": b_sauver}


def initFiltration(request):
    b_listeFiltree = False
    posted = None
    if "appClient" in request.session:
        if "filtrage" in request.session["appClient"]:
            b_listeFiltree = True
            posted = request.session['appClient']['formRechercheClient']
        else:
            request.session["appClient"] = {}
    else:
        request.session["appClient"] = {}

    request.session.modified = True
    return {'posted': posted, 'b_listeFiltree': b_listeFiltree}


def filtration(request):
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
        return {'filtrage': filtrage, 'b_listeFiltree': b_listeFiltree}
