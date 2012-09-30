from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.inclusion_tag("_inc/l-button.html")
def bt(href, aid, uiiconstyle, text):
    if href == "":
        urltext = ""
    else:
        urltext = reverse(href)

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
            string = "\"" + arg + "\""
        else:
            string = str(arg)

        onclickstr += str(string) + ','

    onclickstr = onclickstr.rstrip(',')
    onclickstr += ")"

    return {'jfunc': onclickstr, 'uiiconstyle': uiiconstyle, 'text': text}


@register.inclusion_tag("_inc/formfield_errors.html")
def ffe(errors):
    return {'errors': errors}
