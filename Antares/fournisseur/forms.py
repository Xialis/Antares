# -*- coding: utf-8 -*-
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from fournisseur.models import *


class FourForm(ModelForm):
    class Meta:
        model = Fournisseur


class TypeForm(ModelForm):
    traitements = ModelMultipleChoiceField(queryset=Traitement.objects.all(), widget=CheckboxSelectMultiple(), required=True)
    diametres = ModelMultipleChoiceField(queryset=Diametre.objects.all(), widget=CheckboxSelectMultiple(), required=True)
    couleurs = ModelMultipleChoiceField(queryset=Couleur.objects.all(), widget=CheckboxSelectMultiple(), required=True)

    class Meta:
        model = Type
        exclude = ('fournisseur',)

    def filtre_fournisseur(self, fid):
        self.fields['traitements'].queryset = Traitement.objects.filter(fournisseur__id=fid)
        self.fields['diametres'].queryset = Diametre.objects.filter(fournisseur__id=fid)
        self.fields['couleurs'].queryset = Couleur.objects.filter(fournisseur__id=fid)


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
