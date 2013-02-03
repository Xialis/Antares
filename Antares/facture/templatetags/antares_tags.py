# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from Antares.common import NORM, MILLE

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
    t = prescription.transposition()
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

    return {'sphere': NORM(sphere), 'cylindre': NORM(cylindre), 'axe': axe, 'addition': NORM(addition)}


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


@register.filter(name='email')
def email(value):
    if value is not None or value != "":
        s = '<a href="mailto:%s">%s</a>' % (escape(value), escape(value))
        return mark_safe(s)
    else:
        return ""
