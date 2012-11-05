# -*- coding: utf-8 -*-

# import python
from datetime import date

# import django
from django.core.exceptions import ObjectDoesNotExist

# import Antares
from commande.models import Commande, LigneCommande


def ajouterPrescription(ligneFacture):
    """
    Ajoute un/deux verres de prescriptions à la commande en cours
    """

    # On récupère la commande en cours
    commande = nouvelleCommande(ligneFacture.vtype.fournisseur)

    lc = LigneCommande()
    lc.commande = commande
    lc.ligne_facture = ligneFacture

    if ligneFacture.oeil == 'T':
        lc.quantite = 2
    else:
        lc.quantite = 1

    lc.save()
    return True


def nouvelleCommande(fournisseur):
    """
    Créé une nouvelle commande
    Si la commande existe déjà et date_envoi est None alors on ne créé rien.
    """

    courante = None
    try:
        courante = Commande.objects.filter(fournisseur=fournisseur).latest('id')
    except ObjectDoesNotExist:
        # Première commande ;-)
        courante = None

    if courante is None or courante.date_envoi is not None:
        # Nouvelle commande
        commande = Commande()
        numero = 0
        try:
            derniere = Commande.objects.filter(fournisseur=fournisseur).latest('id')
            numero = derniere.numero
        except ObjectDoesNotExist:
            pass

        commande.numero = unicode(int(numero) + 1)
        commande.fournisseur = fournisseur
        commande.save()
        return commande
    else:
        # Commande en cours
        return courante


def validerCommande(commande):
    """
    Valider une commande (clore)
    Ajoute la date d'envoi
    S'il n'y a pas de LigneCommande, empécher la validation
    Ajouter les verres de stock
    """
    # TODO: voir views commandeF pour gérer la commande stock
    if commande.lignecommande_set.count() != 0:
        commande.date_envoi = date.today()
        commande.save()
        return True

    return False
