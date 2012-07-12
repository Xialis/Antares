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

        sphere = cd.get('sphere')
        cylindre = cd.get('cylindre')
        addition = cd.get('addition')

        if sphere and sphere % Decimal('0.25') != 0:
            msg = u"Il faut un multiple de 0.25"
            self._errors['sphere'] = self.error_class([msg])
            del cd['sphere']

        if cylindre and cylindre % Decimal('0.25') != 0:
            msg = u"Il faut un multiple de 0.25"
            self._errors['cylindre'] = self.error_class([msg])
            del cd['cylindre']
            
        if addition and addition % Decimal('0.25') != 0:
            msg = u"Il faut un multiple de 0.25"
            self._errors['addition'] = self.error_class([msg])
            del cd['addition']

        return cd
