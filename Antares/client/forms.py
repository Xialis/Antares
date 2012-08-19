# -*- coding: utf-8 -*-
from decimal import Decimal
from django.forms import Form, ModelForm, DecimalField, HiddenInput, CharField, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple

from Antares.common import jq_datefield
from client.models import *


class FormAjoutClient(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Client
        exclude = ('code')


class FormAjoutOrganisme(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = OrganismePayeur


class FormAjoutPrescripteur(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Prescripteur


class FormRechercheClient(ModelForm):

    class Meta:
        model = Client

    def __init__(self, *args, **kwargs):
        super(FormRechercheClient, self).__init__(*args, **kwargs)

        for fieldname in self.base_fields:
            self.base_fields[fieldname].required = False


class FormAjoutPrescription(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    formfield_callback = jq_datefield

    class Meta:
        model = Prescription
        exclude = ('erreur', 'client', )

    def clean(self):
        cd = self.cleaned_data
        
        champs = ['axe_od', 'axe_og']
        for champ in champs:
            valeur = cd.get(champ)
            if valeur:
                if valeur < 0 or valeur >= 180:
                    msg = u"L'axe doit être compris entre 0 (inclus) et 180 (exclus)"
                    self._errors[champ] = self.error_class([msg])
                    del cd[champ]

                if not cd.get('cylindre_' + champ[-2:]):
                    msg = u"Ce champ est obligatoire (axe spécifié)"
                    self._errors['cylindre_' + champ[-2:]] = self.error_class([msg])
                    if cd.get('cylindre_' + champ[-2:]):
                        del cd['cylindre_' + champ[-2:]]

        champs = ['cylindre_od', 'cylindre_og']
        for champ in champs:
            valeur = cd.get(champ)
            if valeur and not cd.get('axe_' + champ[-2:]):
                msg = u"Ce champ est obligatoire (cylindre spécifié)"
                self._errors['axe_' + champ[-2:]] = self.error_class([msg])
                del cd['axe_' + champ[-2:]]
                
        champs = ['sphere_od', 'cylindre_od', 'addition_od', 'sphere_og', 'cylindre_og', 'addition_og']
        for champ in champs:
            valeur = cd.get(champ)
            if valeur and valeur % Decimal('0.25') != 0:
                msg = u"Il faut un multiple de 0.25"
                self._errors[champ] = self.error_class([msg])
                del cd[champ]

        
        return cd

