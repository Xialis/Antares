# -*- coding: utf-8 -*-
from decimal import Decimal
from django.forms import Form, ModelForm, DecimalField, HiddenInput, CharField, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple

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
