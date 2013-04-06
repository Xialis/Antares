# -*- coding: utf-8 -*-
from django.db import models


class Facture(models.Model):
    numero = models.CharField(max_length=12, unique=True)
    date_creation = models.DateField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    client = models.ForeignKey('client.Client')
    prescription = models.ForeignKey('client.Prescription')
    bproforma = models.BooleanField(verbose_name=u"PRO FORMA ?", default=True, help_text=u"Décocher la case pour créer directement une facture.")
    proforma = models.ForeignKey('self', blank=True, null=True)
    interlocuteur = models.ForeignKey('facture.Interlocuteur')
    organisme = models.ForeignKey('client.OrganismePayeur', blank=True, null=True)
    solde = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    def total(self):
        total = 0
        lfs = self.lignefacture_set.all()
        for lf in lfs:
            total += lf.tarif

        os = self.option_set.all()
        for o in os:
            total += o.tarif

        ms = self.monture_set.all()
        for m in ms:
            total += m.tarif

        return total

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
    traitement = models.ForeignKey('fournisseur.Traitement')
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

        remise_supplements = trm + crm

        if self.vtype.progressif == True:
            remise_supplements = remise_supplements * 2

        if self.oeil == 'T':
            remise += (vrm + remise_supplements) * 2
        else:
            remise += (vrm + remise_supplements)

        return remise

    def calculTotal(self):
        tarif_type = self.vtype.tarif
        tarif_couleur = self.couleur.tarif
        tarif_traitement = self.traitement.tarif

        total_supplements = tarif_couleur + tarif_traitement

        if self.vtype.progressif == True:
            total_supplements = total_supplements * 2

        total = tarif_type + total_supplements
        return total


class Option(models.Model):
    facture = models.ForeignKey('facture.Facture')
    nom = models.CharField(max_length=50)
    tarif = models.DecimalField(max_digits=8, decimal_places=0)


class Interlocuteur(models.Model):
    nom = models.CharField(max_length=25, unique=True)

    def __unicode__(self):
        return self.nom

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
