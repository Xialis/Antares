# -*- coding: utf-8 -*-
from django.forms import ModelForm
from facture.models import LigneFacture


class LigneForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    
    class Meta:
        model = LigneFacture
        exclude = ('facture', )

