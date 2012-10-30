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

    class Meta:
        ordering = ['nom']
        unique_together = ('nom', 'telephone')


class Client(models.Model):
    code = models.CharField(max_length=12)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return self.nom + " " + self.prenom

    class Meta:
        unique_together = (('nom', 'prenom', 'telephone'), ('nom', 'prenom', 'email'), )
        ordering = ['code']


class Prescription(models.Model):
    prescripteur = models.ForeignKey('client.Prescripteur')
    client = models.ForeignKey('client.Client')
    date_realisation = models.DateField()
    erreur = models.BooleanField()

    sphere_od = models.DecimalField(max_digits=4, decimal_places=2)
    cylindre_od = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    addition_od = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    axe_od = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    sphere_og = models.DecimalField(max_digits=4, decimal_places=2)
    cylindre_og = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    addition_og = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    axe_og = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

    def __unicode__(self):
        return self.prescripteur.nom + " c: " + self.client.nom
