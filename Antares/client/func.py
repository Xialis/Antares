# -*- coding: utf-8 -*-
from datetime import date
from client.models import Client


def ajoutClient(formAjoutClient):

    b_sauver = False
    dj = date.today()

    if formAjoutClient.is_valid():
        client = formAjoutClient.save(commit=False)
        #code
        debut_code = dj.strftime("%Y") + dj.strftime("%m") + dj.strftime("%d")
        compteur = Client.objects.filter(code__startswith=debut_code).count()
        if compteur < 10:
            s_compteur = '00' + str(compteur+1)
        elif compteur < 100:
            s_compteur = '0' + str(compteur+1)

        code = debut_code + s_compteur
        client.code = code
        client.save()
        b_sauver = True

    return {"form": formAjoutClient, "b_sauver": b_sauver}
