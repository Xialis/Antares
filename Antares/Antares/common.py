# -*- coding: utf-8 -*-
from django.db import models


def jq_datefield(f, **kwargs):
    formfield = f.formfield(**kwargs)

    if isinstance(f, models.DateField):
        formfield.widget.format = '%d/%m/%Y'
        formfield.widget.attrs.update({'class': 'datePicker', 'readonly': 'true'})

    return formfield


def NORM(decimal):
    if decimal is None:
        return ""
    return "{0:.2f}".format(decimal)


def MILLE(decimal):
    dstr = str(decimal)
    retour = ""
    compteur = 0
    for x in reversed(xrange(0, len(dstr))):
        if compteur == 3:
            retour = " " + retour
            compteur = 0

        retour = dstr[x] + retour
        compteur += 1

    return retour
