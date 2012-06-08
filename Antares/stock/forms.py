# -*- coding: utf-8 -*-
from decimal import Decimal
from django.forms import ModelForm, HiddenInput, CharField, BooleanField
from stock.models import LigneStock
from fournisseur.models import Type, Traitement, Diametre, Couleur


class AjoutForm(ModelForm):
    fid = CharField(widget=HiddenInput)

    class Meta:
        model = LigneStock
        exclude = ('fournisseur', )

    def filtre_fournisseur(self, fid):
        self.fields['vtype'].queryset = Type.objects.filter(fournisseur__id=fid).filter(stock=True)
        self.fields['traitement'].queryset = Traitement.objects.filter(fournisseur__id=fid)
        self.fields['diametre'].queryset = Diametre.objects.filter(fournisseur__id=fid)
        self.fields['couleur'].queryset = Couleur.objects.filter(fournisseur__id=fid)
        self.fields['fid'].initial = fid
        return self
    
    def pasdechoix(self):
        self.fields['traitement'].queryset = Traitement.objects.filter(fournisseur__id=9999)
        self.fields['diametre'].queryset = Diametre.objects.filter(fournisseur__id=9999)
        self.fields['couleur'].queryset = Couleur.objects.filter(fournisseur__id=9999)
        return self
    
    def clean(self):
        cd = self.cleaned_data
        
        sphere = cd.get('sphere')
        cylindre = cd.get('cylindre')
        
        if sphere and sphere % Decimal('0.25') != 0:
            msg = u"Il faut un multiple de 0.25"
            self._errors['sphere'] = self.error_class([msg])
            del cd['sphere']
            
        if cylindre and cylindre % Decimal('0.25') != 0:
            msg = u"Il faut un multiple de 0.25"
            self._errors['cylindre'] = self.error_class([msg])
            del cd['cylindre']
        
        return cd


class ModificationForm(ModelForm):
    lid = CharField(widget=HiddenInput)
    supprimer = BooleanField()

    class Meta:
        model = LigneStock
        fields = ('quantite', 'seuil')
