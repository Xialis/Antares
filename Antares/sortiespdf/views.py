# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import black, grey, lightgrey, white
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO

from django.http import HttpResponse

from Antares.common import NORM
from facture.models import Facture

import os
APP_ROOT = os.path.dirname(os.path.realpath(__file__))


def facture(request, fid):
    """
    Géneration du pdf facture/proforma
    """

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fid.pdf"'

    reportlab.rl_config.warnOnMissingFontGlyphs = 0
    pdfmetrics.registerFont(TTFont('Vera', os.path.join(APP_ROOT, 'fonts/Vera.ttf')))
    pdfmetrics.registerFont(TTFont('VeraBd', os.path.join(APP_ROOT, 'fonts/VeraBd.ttf')))
    pdfmetrics.registerFont(TTFont('VeraIt', os.path.join(APP_ROOT, 'fonts/VeraIt.ttf')))
    pdfmetrics.registerFont(TTFont('VeraBI', os.path.join(APP_ROOT, 'fonts/VeraBI.ttf')))

    h, w = A4  # 210 x 297

    tampon = BytesIO()
    p = canvas.Canvas(tampon)

    otext = p.beginText()
    otext.setTextOrigin(10 * mm, 277 * mm)
    otext.setFont('VeraBd', 16)
    otext.textLines('''
    OPTIMAL s.a.r.l
    ESPACE OPTIQUE BAMAKOIS
    ''')
    p.drawText(otext)
    otext.setFont('Vera', 8)
    otext.textLines('''
    Medina-Coura bd du Peuple face I.O.T.A
    BP E4388
    Bamako MALI''')
    p.drawText(otext)

    # -- Table client
    f = Facture.objects.get(id=fid)
    data = [[u'Code client', f.client.code],
            [u'Nom', f.client.nom],
            [u'Prénom', f.client.prenom],
            [u'Tel', f.client.telephone],
            [u'Email', f.client.email]]

    t = Table(data, colWidths=[22 * mm, 73 * mm])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, 4), lightgrey),
                           ('GRID', (0, 0), (-1, -1), 0.5, black),
                           ('FONT', (0, 0), (-1, -1), 'Vera'),
                           ('FONTSIZE', (0, 0), (-1, -1), 8),
                           ('TOPPADDING', (0, 0), (-1, -1), 2),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ]))

    t.wrapOn(p, h, w)
    t.drawOn(p, 105 * mm, 258 * mm)
    # -- fin Table Client

    otext = p.beginText()
    otext.setTextOrigin(10 * mm, 245 * mm)
    otext.setFont('Vera', 10)
    otext.textLine(u"FACTURE n°: " + f.numero + u" du " + f.date_creation.strftime("%d / %m / %Y"))
    otext.textLine(u"Votre interlocuteur: " + f.interlocuteur.nom)
    p.drawText(otext)

    # -- Tables prescription
    p.setStrokeColor(black)
    p.setLineWidth(1)
    p.setFillColor(lightgrey)
    p.roundRect(10 * mm, 220 * mm, 85 * mm, 9 * mm, 2 * mm, stroke=0, fill=1)
    p.setFillColor(black)
    otext = p.beginText()
    otext.setTextOrigin(15 * mm, 223 * mm)
    otext.setFont('VeraBd', 12)
    otext.textLine(u"Prescription")
    p.drawText(otext)
    
    otext = p.beginText()
    otext.setTextOrigin(15 * mm, 216 * mm)
    otext.setFont('Vera', 8)
    otext.textLine(u"Prescripteur: " + f.prescription.prescripteur.nom)
    p.drawText(otext)
    
    sphere_od = NORM(f.prescription.sphere_od)
    cylindre_od = NORM(f.prescription.cylindre_od)
    if f.prescription.axe_od is None:
        axe_od = str(f.prescription.axe_od) + " °"
    else:
        axe_od = ""
    addition_od = NORM(f.prescription.addition_od)

    sphere_og = NORM(f.prescription.sphere_og)
    cylindre_og = NORM(f.prescription.cylindre_og)
    if f.prescription.axe_og is None:
        axe_og = str(f.prescription.axe_og) + " °"
    else:
        axe_og = ""
    addition_og = NORM(f.prescription.addition_og)

    datap = [['', u"SPHERE", u"CYLINDRE", u"AXE", u"ADDITION"],
             [u"OD", sphere_od, cylindre_od, axe_od, addition_od],
             [u"OG", sphere_og, cylindre_og, axe_og, addition_og]]

    t = Table(datap, colWidths=15 * mm)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, -1), lightgrey),
                           ('BACKGROUND', (0, 0), (-1, 0), lightgrey),
                           ('GRID', (0, 0), (-1, -1), 0.5, black),
                           ('FONT', (0, 0), (-1, -1), 'Vera'),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('TOPPADDING', (0, 0), (-1, -1), 2),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('LEFTPADDING', (0, 0), (-1, -1), 2),
                           ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('BACKGROUND', (0, 0), (0, 0), white),
                           ]))

    t.wrapOn(p, h, w)
    t.drawOn(p, 13 * mm, 200 * mm)

    otext = p.beginText()
    otext.setTextOrigin(15 * mm, 195 * mm)
    otext.setFont('Vera', 8)
    otext.textLine(u"Formule commandée (norme internationale): ")
    p.drawText(otext)

    ptrans = f.prescription.transposition()
    tsphere_od = NORM(ptrans.sphere_od)
    tcylindre_od = NORM(ptrans.cylindre_od)
    if ptrans.axe_od is None:
        taxe_od = str(ptrans.axe_od) + " °"
    else:
        taxe_od = ""
    taddition_od = NORM(ptrans.addition_od)

    tsphere_og = NORM(ptrans.sphere_og)
    tcylindre_og = NORM(ptrans.cylindre_og)
    if ptrans.axe_og is None:
        taxe_og = str(ptrans.axe_og) + " °"
    else:
        taxe_og = ""
    taddition_og = NORM(ptrans.addition_og)
    datat = [['', u"SPHERE", u"CYLINDRE", u"AXE", u"ADDITION"],
             [u"OD", tsphere_od, tcylindre_od, taxe_od, taddition_od],
             [u"OG", tsphere_og, tcylindre_og, taxe_og, taddition_og]]

    t = Table(datat, colWidths=15 * mm)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (0, -1), lightgrey),
                           ('BACKGROUND', (0, 0), (-1, 0), lightgrey),
                           ('GRID', (0, 0), (-1, -1), 0.5, black),
                           ('FONT', (0, 0), (-1, -1), 'Vera'),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('TOPPADDING', (0, 0), (-1, -1), 2),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('LEFTPADDING', (0, 0), (-1, -1), 2),
                           ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('BACKGROUND', (0, 0), (0, 0), white),
                           ]))

    t.wrapOn(p, h, w)
    t.drawOn(p, 13 * mm, 179 * mm)
    # -- Fin tables prescription

    # -- Equipements
    p.setStrokeColor(black)
    p.setLineWidth(1)
    p.setFillColor(lightgrey)
    p.roundRect(105 * mm, 220 * mm, 95 * mm, 9 * mm, 2 * mm, stroke=0, fill=1)
    p.setFillColor(black)
    otext = p.beginText()
    otext.setTextOrigin(110 * mm, 223 * mm)
    otext.setFont('VeraBd', 12)
    otext.textLine(u"Equipements")
    p.drawText(otext)
    # -- Fin équipements

    # -- ligne de séparation
    p.setStrokeColor(black)
    p.setLineWidth(1)
    p.setLineJoin(0)
    lineslist = [[10 * mm, 70 * mm, 200 * mm, 70 * mm], [10 * mm, 69 * mm, 200 * mm, 69 * mm]]
    p.lines(lineslist)
    # -- fin de ligne de séparation
    p.showPage()
    p.save()

    pdf = tampon.getvalue()
    tampon.close()
    response.write(pdf)
    return response
