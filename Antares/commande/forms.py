# -*- coding: utf-8 -*-
from django.forms import Form, ModelForm, IntegerField, HiddenInput


class ComRecepForm(Form):
    error_css_class = 'error'
    required_css_class = 'required'

    recu = IntegerField(verbose_name=u"reçu")
    lignecommande_id = HiddenInput()
