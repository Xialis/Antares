# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from models import Type
from stock.models import LigneStock

from facture.func import transposition


def RechercheVerres(form):

    liste = Type.objects.all()
    return liste


def stock_ou_commande(t_lignefacture):
    """
    Recherche verre en stock des fournisseurs

    t_lignefacture -- liste table de LigneFacture

    Si trouvé : maj stock
    Sinon : ajout à la commande en cours

    """

    for l in t_lignefacture:
        prescription = transposition(l.facture.prescription)

        if l.oeil == 'T':
            # Une lignefacture = 2 verres même type mais formules potentiellement dif.)
            try:
                vstock_od = LigneStock.objects.get(vtype__pk=l.vtype.id,
                                        diametre__pk=l.diametre.id,
                                        couleur__pk=l.couleur.id,
                                        traitement__pk=l.traitement.id,
                                        sphere=prescription.sphere_od,
                                        cylindre=prescription.cylindre_od
                                        )
            except ObjectDoesNotExist:
                # Pas géré par le stock: on commande
                pass  # TODO: Ajouter à la commande
            else:
                vstock_od.quantite = vstock_od.quantite - 1
                vstock_od.save()

            try:
                vstock_og = LigneStock.objects.get(vtype__pk=l.vtype.id,
                                        diametre__pk=l.diametre.id,
                                        couleur__pk=l.couleur.id,
                                        traitement__pk=l.traitement.id,
                                        sphere=prescription.sphere_og,
                                        cylindre=prescription.cylindre_og
                                        )
            except ObjectDoesNotExist:
                pass  # TODO: Ajouter à la commande
            else:
                vstock_og.quantite = vstock_og.quantite - 1
                vstock_og.save()

        else:
            # Un seul verre à traiter (OD ou OG)
            try:
                vstock = LigneStock.objects.get(vtype__pk=l.vtype.id,
                                        diametre__pk=l.diametre.id,
                                        couleur__pk=l.couleur.id,
                                        traitement__pk=l.traitement.id,
                                        sphere=prescription.__getattribute__('sphere_o' + l.oeil.lower()),
                                        cylindre=prescription.__getattribute__('cylindre_o' + l.oeil.lower())
                                        )
            except ObjectDoesNotExist:
                pass  # TODO: Ajouter à la commande
            else:
                vstock.quantite = vstock.quantite - 1
                vstock.save()

    return True
