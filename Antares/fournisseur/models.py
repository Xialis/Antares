# -*- coding: utf-8 -*-
from django.db import models


class Fournisseur(models.Model):
    """ Représente un fournisseur """
    nom = models.CharField(max_length=50, unique=True)
    tel = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    def __unicode__(self):
        return self.nom


class Traitement(models.Model):
    """ Traitement (lié à un fournisseur) """
    fournisseur = models.ForeignKey(Fournisseur)
    nom = models.CharField(max_length=50)
    tarif = models.DecimalField(max_digits=8, decimal_places=0)
    remise_monture = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    def __unicode__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        unique_together = ('fournisseur', 'nom')


class Diametre(models.Model):
    """ Diametre (lié à un fournisseur) """
    fournisseur = models.ForeignKey(Fournisseur)
    nom = models.CharField(max_length=10)

    def __unicode__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        unique_together = ('fournisseur', 'nom')


class Couleur(models.Model):
    """ Couleur du verre """
    fournisseur = models.ForeignKey(Fournisseur)
    nom = models.CharField(max_length=20)
    tarif = models.DecimalField(max_digits=8, decimal_places=0)
    remise_monture = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    def __unicode__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        unique_together = ('fournisseur', 'nom')


class Type(models.Model):
    """ Type de verre (lié à un fournisseur)"""
    fournisseur = models.ForeignKey(Fournisseur)
    nom = models.CharField(max_length=50)
    stock = models.BooleanField()
    progressif = models.BooleanField()
    traitements = models.ManyToManyField(Traitement, blank=True, null=True)
    diametres = models.ManyToManyField(Diametre)
    couleurs = models.ManyToManyField(Couleur, blank=True, null=True)
    tarif = models.DecimalField(max_digits=8, decimal_places=0)
    remise_monture = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    
    def __unicode__(self):
        return self.nom

    class Meta:
        ordering = ['nom']
        unique_together = ('fournisseur', 'nom')

