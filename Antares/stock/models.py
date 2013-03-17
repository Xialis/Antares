# -*- coding: utf-8 -*-
from django.db import models


class LigneStock(models.Model):
    fournisseur = models.ForeignKey('fournisseur.Fournisseur')
    vtype = models.ForeignKey('fournisseur.Type', verbose_name=u"type")
    diametre = models.ForeignKey('fournisseur.Diametre')
    sphere = models.DecimalField(max_digits=4, decimal_places=2)
    cylindre = models.DecimalField(max_digits=4, decimal_places=2)
    traitement = models.ForeignKey('fournisseur.Traitement')
    couleur = models.ForeignKey('fournisseur.Couleur')
    quantite = models.IntegerField(verbose_name=u"quantité")
    seuil = models.IntegerField()

    class Meta:
        ordering = ["vtype__nom", "traitement__nom", "couleur__nom", "diametre__nom", "sphere", "cylindre"]
