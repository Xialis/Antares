# -*- coding: utf-8 -*-
from django.forms import ModelForm
from fournisseur.models import *


class FourForm(ModelForm):
    class Meta:
        model = Fournisseur


class TypeForm(ModelForm):
    class Meta:
        model = Type
        exclude = ('fournisseur',)


class TraitementForm(ModelForm):
    class Meta:
        model = Traitement
        exclude = ('fournisseur',)


class DiametreForm(ModelForm):
    class Meta:
        model = Diametre
        exclude = ('fournisseur',)


class CouleurForm(ModelForm):
    class Meta:
        model = Couleur
        exclude = ('fournisseur',)
