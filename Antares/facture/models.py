# -*- coding: utf-8 -*-
from django.db import models


class Facture(models.Model):
    numero = models.CharField(max_length=12, unique=True)
    date_creation = models.DateField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    client = models.ForeignKey('client.Client')
    prescription = models.ForeignKey('client.Prescription')
    bproforma = models.BooleanField(verbose_name=u"PRO FORMA ?", default=True)
    proforma = models.ForeignKey('self', blank=True, null=True)
    interlocuteur = models.ForeignKey('facture.Interlocuteur')
    organisme = models.ForeignKey('client.OrganismePayeur', blank=True, null=True)
    solde = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

OEIL = (
        ('T', 'ODG'),
        ('D', 'OD'),
        ('G', 'OG'),
    )


class LigneFacture(models.Model):
    facture = models.ForeignKey('Facture')
    monture = models.PositiveIntegerField()  # Correspondance verres -> monture
    oeil = models.CharField(max_length=1, choices=OEIL)
    vtype = models.ForeignKey('fournisseur.Type', verbose_name="type")
    diametre = models.ForeignKey('fournisseur.Diametre')
    couleur = models.ForeignKey('fournisseur.Couleur')
    traitement = models.ForeignKey('fournisseur.Traitement', blank=True, null=True)
    tarif = models.DecimalField(max_digits=8, decimal_places=0)
    remise_monture = models.DecimalField(max_digits=8, decimal_places=0)


class Option(models.Model):
    facture = models.ForeignKey('facture.Facture')
    nom = models.CharField(max_length=50)
    tarif = models.DecimalField(max_digits=8, decimal_places=0)


class Interlocuteur(models.Model):
    nom = models.CharField(max_length=25, unique=True)

VISION = (
          ('P', 'Près'),
          ('L', 'Loin'),
          ('M', 'Progressif'),
          )


class Monture(models.Model):
    facture = models.ForeignKey('facture.Facture')
    numero = models.PositiveIntegerField()  # Correspondance verres -> monture
    nom = models.CharField(max_length=50, blank=True, null=True)
    tarif = models.DecimalField(max_digits=8, decimal_places=0)
    vision = models.CharField(max_length=1, choices=VISION)
    oeil = models.CharField(max_length=1, choices=OEIL, default='T')
