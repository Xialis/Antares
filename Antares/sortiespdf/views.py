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
from facture.models import Facture, Monture

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
    if f.bproforma == True:
        otext.textLine(u"PRO FORMA n°: " + f.numero + u" du " + f.date_creation.strftime("%d / %m / %Y"))
    else:
        otext.textLine(u"FACTURE n°: " + f.numero + u" du " + f.date_creation.strftime("%d / %m / %Y"))
    otext.textLine(u"Votre interlocuteur: " + f.interlocuteur.nom)
    p.drawText(otext)

    # -- Tables prescription
    titre(10 * mm, 220 * mm, 80 * mm, u"Prescription", p)
    
    otext = p.beginText()
    otext.setTextOrigin(15 * mm, 216 * mm)
    otext.setFont('Vera', 8)
    otext.textLine(u"Prescripteur: " + f.prescription.prescripteur.nom)
    p.drawText(otext)
    
    sphere_od = NORM(f.prescription.sphere_od)
    cylindre_od = NORM(f.prescription.cylindre_od)
    if f.prescription.axe_od is not None:
        axe_od = str(f.prescription.axe_od) + " °"
    else:
        axe_od = ""
    addition_od = NORM(f.prescription.addition_od)

    sphere_og = NORM(f.prescription.sphere_og)
    cylindre_og = NORM(f.prescription.cylindre_og)
    if f.prescription.axe_og is not None:
        axe_og = str(f.prescription.axe_og) + " °"
    else:
        axe_og = ""
    addition_og = NORM(f.prescription.addition_og)

    date_realisation = f.prescription.date_realisation
    str_date = date_realisation.strftime("%d/%m/%y")

    datap = [[str_date, u"SPHERE", u"CYLINDRE", u"AXE", u"ADDITION"],
             [u"OD", sphere_od, cylindre_od, axe_od, addition_od],
             [u"OG", sphere_og, cylindre_og, axe_og, addition_og]]

    t = Table(datap, colWidths=15 * mm)
    tstyle = TableStyle([('BACKGROUND', (0, 0), (0, -1), lightgrey),
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
                           ])

    t.setStyle(tstyle)
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
    if ptrans.axe_od is not None:
        taxe_od = str(ptrans.axe_od) + " °"
    else:
        taxe_od = ""
    taddition_od = NORM(ptrans.addition_od)

    tsphere_og = NORM(ptrans.sphere_og)
    tcylindre_og = NORM(ptrans.cylindre_og)
    if ptrans.axe_og is not None:
        taxe_og = str(ptrans.axe_og) + " °"
    else:
        taxe_og = ""
    taddition_og = NORM(ptrans.addition_og)
    datat = [['', u"SPHERE", u"CYLINDRE", u"AXE", u"ADDITION"],
             [u"OD", tsphere_od, tcylindre_od, taxe_od, taddition_od],
             [u"OG", tsphere_og, tcylindre_og, taxe_og, taddition_og]]

    t = Table(datat, colWidths=15 * mm)
    t.setStyle(tstyle)

    t.wrapOn(p, h, w)
    t.drawOn(p, 13 * mm, 179 * mm)
    
    otext = p.beginText()
    otext.setTextOrigin(12 * mm, 175 * mm)
    otext.setFont('Vera', 8)
    otext.textLine(u"Informations sur votre vue:")
    otext.textLine(u"- Amétropie (OD/OG): " + f.prescription.ametropie())
    otext.textLine(u"- Astigmatisqme (OD/OG): " + f.prescription.astigmatisme())
    otext.textLine(u"- Presbytie: " + f.prescription.presbytie())
    p.drawText(otext)
    # -- Fin tables prescription

    # -- Equipements
    testyle = TableStyle([('BACKGROUND', (0, 0), (1, 0), lightgrey),
                           ('BACKGROUND', (4, 0), (5, 0), lightgrey),
                           ('BACKGROUND', (2, 1), (3, 1), lightgrey),
                           ('GRID', (0, 0), (-1, -1), 0.5, black),
                           ('FONT', (0, 0), (-1, -1), 'Vera'),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('TOPPADDING', (0, 0), (-1, -1), 2),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('LEFTPADDING', (0, 0), (-1, -1), 2),
                           ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                           ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                           ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                           ('ALIGN', (3, 0), (3, -1), 'LEFT'),
                           ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
                           ('ALIGN', (5, 0), (5, -1), 'LEFT'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ])

    titre(95 * mm, 220 * mm, 105 * mm, u"Equipements (" + str(Monture.objects.filter(facture_id=fid).count()) + ")", p)

    monture_suivante = True
    ypos = 218 * mm
    for lf in f.lignefacture_set.all().order_by('oeil').order_by('monture'):

        if monture_suivante == True:
            monture_suivante = False
            ypos -= 2 * mm
            monture = Monture.objects.get(facture_id=fid, numero=lf.monture)
            otext = p.beginText()
            otext.setTextOrigin(100 * mm, ypos)
            otext.setFont('Vera', 8)
            otext.textOut(u"Monture: " + monture.nom + ":: Tarif: " + str(monture.tarif))
            p.drawText(otext)
            xpos, ypos = otext.getCursor()
            ypos -= 1 * mm

        datae = [[u"Oeil", "", u"Type", "", u"Couleur", ""],
                 [u"Ø", "", u"Trait.", "", u"Tarif", ""]
                ]
        if lf.oeil == 'T':
            datae[0][1] = u"ODG"
            monture_suivante = True
        else:
            datae[0][1] = u"O" + lf.oeil
            monture_suivante = False

        if lf.oeil == 'G':
            monture_suivante = True

        datae[0][3] = lf.vtype.nom
        datae[0][5] = lf.couleur.nom
        datae[1][1] = lf.diametre.nom
        datae[1][3] = lf.traitement.nom
        datae[1][5] = lf.tarif

        t = Table(datae, colWidths=[10 * mm, 10 * mm, 12 * mm, 28 * mm, 12 * mm, 28 * mm])
        t.setStyle(testyle)
    
        w, h = t.wrapOn(p, h, w)
        t.drawOn(p, 98 * mm, ypos - h)
        ypos = ypos - h - (2 * mm)
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


def titre(x, y, l, texte, p):
    p.setStrokeColor(black)
    p.setLineWidth(1)
    p.setFillColor(lightgrey)
    p.roundRect(x, y, l, 9 * mm, 2 * mm, stroke=0, fill=1)
    p.setFillColor(black)
    otext = p.beginText()
    otext.setTextOrigin(x + 5 * mm, y + 3 * mm)
    otext.setFont('VeraBd', 12)
    otext.textLine(texte)
    p.drawText(otext)
