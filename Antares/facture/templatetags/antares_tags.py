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
