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
