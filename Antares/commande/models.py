# -*- coding: utf-8 -*-
from django.db import models


class Commande(models.Model):
    numero = models.CharField(max_length=12)
    date_creation = models.DateField(auto_now_add=True)
    date_envoi = models.DateField(blank=True, null=True)
    fournisseur = models.ForeignKey("fournisseur.Fournisseur")

    def __unicode__(self):
        return self.numero


class LigneCommande(models.Model):
    commande = models.ForeignKey("commande.Commande")
    ligne_facture = models.ForeignKey("facture.LigneFacture", null=True, blank=True)  # Seulement en cas de verre de prescription
    ligne_stock = models.ForeignKey("stock.LigneStock", null=True, blank=True)  # Seulement en cas de verre de prescription
    quantite = models.IntegerField(verbose_name=u"quantité")
    quantite_recu = models.IntegerField(verbose_name=u"quantité reçue", default=0)

    def __unicode__(self):
        return u'pour Commande ' + self.commande.numero
