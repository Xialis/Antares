# -*- coding: utf-8 -*-
from django.db import models


class OrganismePayeur(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    contact_nom = models.CharField(max_length=50)
    contact_tel = models.CharField(max_length=50)
    contact_mail = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return self.nom


class Prescripteur(models.Model):
    nom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.nom


class Client(models.Model):
    code = models.CharField(max_length=12)
    date_ajout = models.DateField()
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    organisme = models.ForeignKey('client.OrganismePayeur', blank=True, null=True)

    def __unicode__(self):
        return self.nom + " " + self.prenom


class Prescription(models.Model):
    prescripteur = models.ForeignKey('client.Prescripteur')
    client = models.ForeignKey('client.Client')
    date_realisation = models.DateField()
    erreur = models.BooleanField()

    sphere = models.DecimalField(max_digits=4, decimal_places=2)
    cylindre = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    addition = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    axe = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

    def __unicode__(self):
        return self.prescripteur + " c: " + self.client.nom
