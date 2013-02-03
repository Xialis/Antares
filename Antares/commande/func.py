# -*- coding: utf-8 -*-

# import python
from datetime import date

# import django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

# import Antares
from commande.models import Commande, LigneCommande
from stock.models import LigneStock


def ajouterPrescription(ligneFacture, oeil):
    """
    Ajoute un/deux verres de prescriptions à la commande en cours

    Arguments:
    ligneFacture -- object ligneFacture
    oeil -- oeil à ajouter en prescription
    """

    # On récupère la commande en cours
    commande = nouvelleCommande(ligneFacture.vtype.fournisseur)

    lc = LigneCommande()
    lc.commande = commande
    lc.ligne_facture = ligneFacture
    lc.quantite = 1
    lc.oeil = oeil

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
    listestock = listeStock(commande.fournisseur)
    for l in listestock:
        lc = LigneCommande()
        lc.commande = commande
        lc.ligne_stock = l['lignestock']
        lc.quantite = l['qtacom']
        lc.save()

    if commande.lignecommande_set.count() != 0:
        commande.date_envoi = date.today()
        commande.save()
        return True

    return False


def listeStock(fournisseur):
    """
    retourne la liste des verres de stock à commander
    """

    # gestion commande stock
    liste = []
    listeStock = LigneStock.objects.filter(fournisseur=fournisseur).filter(quantite__lt=F('seuil'))

    for ligne in listeStock:
        diff = ligne.seuil - ligne.quantite
        qtcom = 0  # Quantité déjà commandée
        for lc in LigneCommande.objects.filter(ligne_stock=ligne, quantite__gt=F('quantite_recu')):
            qtcom = qtcom + lc.quantite - lc.quantite_recu

        if diff > qtcom:
            qtacom = diff - qtcom
            liste.append({'lignestock': ligne, 'qtcom': qtcom, 'qtacom': qtacom})

    return liste
