# -*- coding: utf-8 -*-
from client.models import Client


def ajoutClient(formAjoutClient):

    b_sauver = False
    if formAjoutClient.is_valid():
        return 0
    
    return {"form": formAjoutClient, "sauver": b_sauver}
