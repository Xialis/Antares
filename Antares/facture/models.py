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

    def calculRemise(self):
        remise = 0
        if self.traitement.remise_monture is None:
            trm = 0
        else:
            trm = self.traitement.remise_monture

        if self.couleur.remise_monture is None:
            crm = 0
        else:
            crm = self.couleur.remise_monture

        if self.vtype.remise_monture is None:
            vrm = 0
        else:
            vrm = self.vtype.remise_monture

        if self.oeil == 'T':
            remise += (trm + crm + vrm) * 2
        else:
            remise += (trm + crm + vrm)

        return remise

    def calculTotal(self):
        tarif_type = self.vtype.tarif
        tarif_couleur = self.couleur.tarif
        tarif_traitement = self.traitement.tarif
        total = tarif_type + tarif_couleur + tarif_traitement
        return total


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
