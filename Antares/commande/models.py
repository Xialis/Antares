# -*- coding: utf-8 -*-
from django.db import models


class Commande(models.Model):
    numero = models.CharField(max_length=12, unique=True)
    date_creation = models.DateField(auto_now_add=True)
    fournisseur = models.ForeignKey("fournisseur.Fournisseur")
