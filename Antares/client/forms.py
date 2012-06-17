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
