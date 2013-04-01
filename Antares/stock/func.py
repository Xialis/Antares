# -*- coding: utf-8 -*-

from stock.models import LigneStock


def modstock(ligneStock, delta):
    ligneStock.quantite = ligneStock.quantite + delta
    ligneStock.save()

    return True


def listevtype(lignesStock):
    retour = []
    dernier_type = ""

    for l in lignesStock:
        if dernier_type != l.vtype.nom:
            dernier_type = l.vtype.nom
            retour.append(dernier_type)

    return retour
