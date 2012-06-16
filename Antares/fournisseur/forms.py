# -*- coding: utf-8 -*-
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, CharField, HiddenInput
from fournisseur.models import Fournisseur, Type, Traitement, Diametre, Couleur


class FourForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Fournisseur


class TypeForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    fid = CharField(widget=HiddenInput)
    traitements = ModelMultipleChoiceField(queryset=Traitement.objects.all(), widget=CheckboxSelectMultiple(), required=False)
    diametres = ModelMultipleChoiceField(queryset=Diametre.objects.all(), widget=CheckboxSelectMultiple(), required=True)
    couleurs = ModelMultipleChoiceField(queryset=Couleur.objects.all(), widget=CheckboxSelectMultiple(), required=False)

    class Meta:
        model = Type
        exclude = ('fournisseur',)

    def filtre_fournisseur(self, fid):
        self.fields['traitements'].queryset = Traitement.objects.filter(fournisseur__id=fid)
        self.fields['diametres'].queryset = Diametre.objects.filter(fournisseur__id=fid)
        self.fields['couleurs'].queryset = Couleur.objects.filter(fournisseur__id=fid)
        self.fields['fid'].initial = fid
        return self

    def erreurDuplica(self):
        msg = u"Ce nom existe déjà pour ce fournisseur"
        self._errors['nom'] = self.error_class([msg])
        return self

    def clean(self):
        cd = self.cleaned_data

        #Test transition
        tt = cd.get("tarif_transition")
        couleurs = cd.get("couleurs")
        transition = False

        if couleurs:
            for c in couleurs:
                if c.transition:
                    transition = True
                    break

        if tt and (not couleurs or not transition):
            msg = u"Vous devez choisir au moins une couleur Transition (tarif spécifié)"
            self._errors['couleurs'] = self.error_class([msg])
            del cd['couleurs']

        if transition and not tt:
            msg = u"Montant nécéssaire (Couleur(s) Transition selectionnée(s)"
            self._errors['tarif_transition'] = self.error_class([msg])
            del cd['tarif_transition']
        #-- Fin test Transition

        return cd


class TraitementForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Traitement
        exclude = ('fournisseur',)

    def erreurDuplica(self):
        msg = u"Ce nom existe déjà pour ce fournisseur"
        self._errors['nom'] = self.error_class([msg])
        return self


class DiametreForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Diametre
        exclude = ('fournisseur',)

    def erreurDuplica(self):
        msg = u"Ce nom existe déjà pour ce fournisseur"
        self._errors['nom'] = self.error_class([msg])
        return self


class CouleurForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Couleur
        exclude = ('fournisseur',)

    def erreurDuplica(self):
        msg = u"Ce nom existe déjà pour ce fournisseur"
        self._errors['nom'] = self.error_class([msg])
        return self
