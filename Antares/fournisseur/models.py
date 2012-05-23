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

    def __unicode__(self):
        return self.nom


class Diametre(models.Model):
    """ Diametre (lié à un fournisseur) """
    fournisseur = models.ForeignKey(Fournisseur)
    nom = models.CharField(max_length=10)

    def __unicode__(self):
        return self.nom


class Couleur(models.Model):
    """ Couleur du verre """
    fournisseur = models.ForeignKey(Fournisseur)
    nom = models.CharField(max_length=20)

    def __unicode__(self):
        return self.nom


class Type(models.Model):
    """ Type de verre (lié à un fournisseur)"""
    fournisseur = models.ForeignKey(Fournisseur)
    nom = models.CharField(max_length=50)
    progressif = models.BooleanField()
    traitements = models.ManyToManyField(Traitement)
    diametres = models.ManyToManyField(Diametre)
    couleurs = models.ManyToManyField(Couleur)

    def __unicode__(self):
        return self.nom
