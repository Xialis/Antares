# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse

from Antares.common import NORM, MILLE
from facture.func import transposition

register = template.Library()


@register.inclusion_tag("_inc/l-button.html")
def bt(aid, uiiconstyle, text, view, *args):
    if view == "":
        urltext = ""
    else:
        urltext = reverse(view, args=args)

    return {'href': urltext, 'aid': aid, 'uiiconstyle': uiiconstyle, 'text': text}


@register.inclusion_tag("_inc/submit-button.html")
def sbt(formID, param, aid, uiiconstyle, text):
    return {'formID': formID, 'param': param, 'aid': aid, 'uiiconstyle': uiiconstyle, 'text': text}


@register.inclusion_tag("_inc/j-button.html")
def jbt(jfunc, aid, uiiconstyle, text, *args):

    onclickstr = jfunc + "("
    for arg in args:

        try:
            float(arg)
        except:
            if arg.lstrip()[0] == '$':
                string = arg
            else:
                string = "'" + arg + "'"
        else:
            string = str(arg)

        onclickstr += str(string) + ','

    onclickstr = onclickstr.rstrip(',')
    onclickstr += ")"

    return {'jfunc': onclickstr, 'uiiconstyle': uiiconstyle, 'text': text}


@register.inclusion_tag("_inc/formfield_errors.html")
def ffe(errors):
    return {'errors': errors}


@register.inclusion_tag("_inc/formule.html")
def formule(prescription, oeil):
    t = transposition(prescription)
    if oeil == 'T' or oeil == 'D':
        sphere = t.sphere_od
        cylindre = t.cylindre_od
        axe = t.axe_od
        addition = t.addition_od
    else:
        sphere = t.sphere_og
        cylindre = t.cylindre_og
        axe = t.axe_og
        addition = t.addition_og

    return {'sphere': sphere, 'cylindre': cylindre, 'axe': axe, 'addition': addition}


@register.filter(name='norm')
def norm(value):
    return NORM(value)


@register.filter(name='mille')
def mille(value):
    return MILLE(value)


@register.filter(name='vision')
def vision(value):
    if value == 'P':
        return u"près"
    elif value == 'L':
        return u"loin"
    else:
        return u"progressif"
