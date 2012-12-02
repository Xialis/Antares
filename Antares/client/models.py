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

    def transposition(self):
        ptrans = Prescription()

        # nouvelle sphere = sphere + cylindre-negatif
        # nouveau cylindre = cylindre-negatif * -1
        # nouvel axe = (axe + 90) % 180 (0<=axe<=179)
        if self.cylindre_od and self.cylindre_od < 0:
            ptrans.sphere_od = self.sphere_od + self.cylindre_od
            ptrans.cylindre_od = abs(self.cylindre_od)
            ptrans.axe_od = (self.axe_od + 90) % 180
        else:
            ptrans.sphere_od = self.sphere_od
            ptrans.cylindre_od = self.cylindre_od
            ptrans.axe_od = self.axe_od

        if self.cylindre_og and self.cylindre_og < 0:
            ptrans.sphere_og = self.sphere_og + self.cylindre_og
            ptrans.cylindre_og = abs(self.cylindre_og)
            ptrans.axe_og = (self.axe_og + 90) % 180
        else:
            ptrans.sphere_og = self.sphere_og
            ptrans.cylindre_og = self.cylindre_og
            ptrans.axe_og = self.axe_og

        ptrans.addition_od = self.addition_od
        ptrans.addition_og = self.addition_og

        return ptrans
