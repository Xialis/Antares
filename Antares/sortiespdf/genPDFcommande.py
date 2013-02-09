# -*- coding: utf-8 -*-
import StringIO
from cgi import escape
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

from commande.models import Commande

import os
APP_ROOT = os.path.dirname(os.path.realpath(__file__))


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    # return HttpResponse(html)
    #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('ISO-8859-15')), result)
    pdf = pisa.CreatePDF(StringIO.StringIO(html.encode('utf-8')), result, encoding='utf-8')
    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + context_dict['commande_select'].fournisseur.nom + '.' + context_dict['commande_select'].numero + '.pdf"'
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def commandepdf(request, cid):
    c = {}
    commande_select = Commande.objects.get(id=cid)
    commandes_ouvertes = Commande.objects.exclude(date_envoi=None).filter(date_cloture=None).exclude(id=cid)

    c['commande_select'] = commande_select
    c['commandes_ouvertes'] = commandes_ouvertes
    c['pagesize'] = 'A4'

    return render_to_pdf('sortiespdf/commandepdf.html', c)
