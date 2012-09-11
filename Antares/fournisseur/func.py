# -*- coding: utf-8 -*-
from forms import RechercheVerresForm
from models import Type


def RechercheVerres(form):
    
    liste = Type.objects.all()
    return liste
