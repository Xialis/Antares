# -*- coding: utf-8 -*-

from stock.models import LigneStock


def modstock(ligneStock, delta):
    ligneStock.quantite = ligneStock.quantite + delta
    ligneStock.save()

    return True
