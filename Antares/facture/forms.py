# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms import HiddenInput, IntegerField, CharField, ModelChoiceField
from facture.models import LigneFacture
from fournisseur.models import Diametre, Couleur, Traitement


class LigneForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    
    diametre = ModelChoiceField(queryset=Diametre.objects.none())
    couleur = ModelChoiceField(queryset=Couleur.objects.none(), required=False)
    traitement = ModelChoiceField(queryset=Traitement.objects.none(), required=False)
    
    class Meta:
        model = LigneFacture
        exclude = ('facture', 'monture', 'oeil', 'tarif')

    def filtre_vtype(self, vtype):
        self.fields['diametre'].queryset = Diametre.objects.filter(type=vtype)
        self.fields['couleur'].queryset = Couleur.objects.filter(type=vtype)
        self.fields['traitement'].queryset = Traitement.objects.filter(type=vtype)
        return self
