# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import black, grey, lightgrey, white
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from io import BytesIO

from django.http import HttpResponse

from Antares.common import NORM, MILLE, visionstr
from facture.models import Facture, Monture

import os
APP_ROOT = os.path.dirname(os.path.realpath(__file__))


def facture(request, fid):
    """
    Géneration du pdf facture/proforma
    """

    f = Facture.objects.get(id=fid)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + f.numero + '.pdf"'

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
    otext.textLines('''OPTIMAL s.a.r.l
    ESPACE OPTIQUE BAMAKOIS''')
    p.drawText(otext)
    otext = p.beginText()
    otext.setFont('Vera', 8)
    otext.setTextOrigin(10 * mm, 265 * mm)
    otext.textLines('''Medina-Coura bd du Peuple face I.O.T.A
    BP E4388
    Bamako MALI''')
    p.drawText(otext)

    # -- Table client
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

    tableauPrescription(13 * mm, 216 * mm,
                        u"Prescripteur: " + f.prescription.prescripteur.nom,
                        f.prescription.date_realisation.strftime("%d/%m/%y"),
                        f.prescription, p)

    vl = vp = vpr = False
    montures = Monture.objects.filter(facture=f)
    for m in montures:
        if m.vision == 'L':
            vl = True
        elif m.vision == 'P':
            vp = True
        else:
            vpr = True

    ystart = 195
    ymarge = 21

    if vl == True:
        tableauPrescription(13 * mm, ystart * mm,
                            u"Formule commandée (norme internationale): ",
                            u"Loin",
                            f.prescription.transposition().vl(), p)
        ystart -= ymarge

    if vp == True:
        tableauPrescription(13 * mm, ystart * mm,
                            u"Formule commandée (norme internationale): ",
                            u"Près",
                            f.prescription.transposition().vp(), p)
        ystart -= ymarge

    if vpr == True:
        tableauPrescription(13 * mm, ystart * mm,
                            u"Formule commandée (norme internationale): ",
                            u"Progressif",
                            f.prescription.transposition(), p)
        ystart -= ymarge

    otext = p.beginText()
    otext.setTextOrigin(12 * mm, (ystart - 2) * mm)
    otext.setFont('Vera', 7)
    otext.textLine(u"Informations sur votre vue:")
    otext.textLine(u"- Amétropie (OD/OG): " + f.prescription.ametropie())
    otext.textLine(u"- Astigmatisqme (OD/OG): " + f.prescription.astigmatisme())
    otext.textLine(u"- Presbytie: " + f.prescription.presbytie())
    p.drawText(otext)
    # -- Fin tables prescription

    # -- Options
    ystart -= 25
    titre(10 * mm, ystart * mm, 80 * mm, u"Options (" + str(f.option_set.all().count()) + ")", p)
    ystart -= 4

    datao = [[u"Désignation", "Tarif"],
            ]
    totalo = 0
    for o in f.option_set.all():
        d = [o.nom, MILLE(o.tarif)]
        totalo += o.tarif
        datao.append(d)

    t = Table(datao, colWidths=30 * mm)
    tstyle = TableStyle([('BACKGROUND', (0, 0), (-1, 0), lightgrey),
                           ('GRID', (0, 0), (-1, -1), 0.5, black),
                           ('FONT', (0, 0), (-1, -1), 'Vera'),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('TOPPADDING', (0, 0), (-1, -1), 2),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('LEFTPADDING', (0, 0), (-1, -1), 2),
                           ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ])

    t.setStyle(tstyle)
    w, h = t.wrapOn(p, h, w)
    t.drawOn(p, 13 * mm, (ystart * mm) - h)
    ystart = ystart - h - (2 * mm)
    # -- fin options

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
    totalverre = 0
    totalmonture = 0
    totalremise = 0
    for lf in f.lignefacture_set.all().order_by('oeil').order_by('monture'):

        totalverre += lf.tarif
        remise = 0
        # Entête
        if monture_suivante == True:
            monture_suivante = False
            ypos -= 2 * mm
            monture = Monture.objects.get(facture_id=fid, numero=lf.monture)
            remise = monture.remise_max()
            totalmonture += monture.tarif
            totalremise += remise

            otext = p.beginText()
            otext.setTextOrigin(100 * mm, ypos)
            otext.setFont('Vera', 8)
            otext.textLine(u"Monture: " + monture.nom + ":: Tarif: " + MILLE(monture.tarif) + " :: Vision: " + visionstr(monture.vision))
            if remise == 0:
                otext.textLine(u"Votre choix de verres ne vous accorde pas de remise sur votre monture.")
            else:
                otext.textLine(u"Votre choix de verres vous accorde une remise de : " + str(remise) + " francs")
            p.drawText(otext)
            xpos, ypos = otext.getCursor()
            ypos -= 0 * mm
        # fin Entête

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
        datae[1][5] = MILLE(lf.tarif)

        t = Table(datae, colWidths=[10 * mm, 10 * mm, 12 * mm, 28 * mm, 12 * mm, 28 * mm])
        t.setStyle(testyle)

        w, h = t.wrapOn(p, h, w)
        t.drawOn(p, 98 * mm, ypos - h)
        ypos = ypos - h - (2 * mm)

    # -- Fin équipements

    # -- Debut Facture
    ypos = ypos - 15 * mm
    if f.bproforma:
        txt = u"Facture PRO FORMA"
    else:
        txt = u"Facture"
    titre(95 * mm, ypos, 105 * mm, txt, p)
    ypos -= 4 * mm
    TOTAL = (totalverre + totalmonture - f.remiseAccordee()) + totalo
    dataf = [[u"Désignation", u"Totaux"],
             [u"Equipement(s)", MILLE(totalverre + totalmonture)],
             [u"Remise sur monture(s)", u"-" + MILLE(f.remiseAccordee())],
             [u"Option(s)", MILLE(totalo)],
             [u"TOTAL à payer", MILLE(TOTAL)]
             ]

    t = Table(dataf, colWidths=[35 * mm, 30 * mm])
    t.setStyle(tstyle)
    w, h = t.wrapOn(p, h, w)
    ypos = ypos - h
    t.drawOn(p, 98 * mm, ypos)

    otext = p.beginText()
    ypos = ypos - 4 * mm
    otext.setTextOrigin(98 * mm, ypos)
    otext.setFont('Vera', 7)
    otext.textLine(u"Arrete la facture à la somme de:")
    otext.textLine(n2l(int(TOTAL)) + " FRANCS CFA")
    otext.textLine("(facture exonerée de T.V.A)")
    p.drawText(otext)
    # -- Fin facture

    # -- Info
    x = 10 * mm
    y = 80 * mm
    otext = p.beginText()
    otext.setTextOrigin(x, y)
    otext.setFont('Vera', 7)
    otext.textLine(u"Informations:")
    otext.textLine(u"- Remises appliquées à chaque montures, en fonction du choix de verres pour cette monture, à concurrence du tarif de la monture")
    p.drawText(otext)
    # -- fin Info

    # -- ligne de séparation
    p.setStrokeColor(black)
    p.setLineWidth(1)
    p.setLineJoin(0)
    lineslist = [[10 * mm, 70 * mm, 200 * mm, 70 * mm], [10 * mm, 69 * mm, 200 * mm, 69 * mm]]
    p.lines(lineslist)
    # -- fin de ligne de séparation

    # -- info bad de page
    x = 10 * mm
    y = 66 * mm
    otext = p.beginText()
    otext.setTextOrigin(x, y)
    otext.setFont('Vera', 7)
    otext.textLine(u"OPTIMAL s.a.r.l")
    otext.textLine(u"ESPACE OPTIQUE BAMAKOIS :: TEL. 20 21 52 27")
    otext.textLine(u"Bon de caisse")
    otext.textLine(u"Interlocuteur: " + f.interlocuteur.nom)
    p.drawText(otext)
    (x, y) = otext.getCursor()

    data = [[u"Date", f.date_creation.strftime("%d / %m / %Y"), u""],
            [u"Montant", MILLE(f.total()), u"F CFA"],
            [u"Avance / déja payé", MILLE(f.total() - f.solde), u"F CFA"],
            [u"Solde", MILLE(f.solde), u"F CFA, à régler à la livraison"],
            ]

    tstyle = TableStyle([('BACKGROUND', (0, 0), (-1, -1), white),
                           ('GRID', (0, 0), (-1, -1), 0.5, black),
                           ('FONT', (0, 0), (-1, -1), 'Vera'),
                           ('FONTSIZE', (0, 0), (-1, -1), 7),
                           ('TOPPADDING', (0, 0), (-1, -1), 2),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                           ('LEFTPADDING', (0, 0), (-1, -1), 2),
                           ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                           ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ])

    t = Table(data, colWidths=[26 * mm, 21 * mm, 40 * mm])
    t.setStyle(tstyle)
    w, h = t.wrapOn(p, h, w)
    y = y - h
    t.drawOn(p, x, y)

    # droite

    x = 110 * mm
    y = 66 * mm
    otext = p.beginText()
    otext.setTextOrigin(x, y)
    otext.setFont('Vera', 7)
    otext.textLine(u"OPTIMAL s.a.r.l")
    otext.textLine(u"ESPACE OPTIQUE BAMAKOIS :: TEL. 20 21 52 27")
    otext.textLine(u"Bon de caisse")
    otext.textLine(u"Interlocuteur: " + f.interlocuteur.nom)
    p.drawText(otext)
    (x, y) = otext.getCursor()
    w, h = t.wrapOn(p, h, w)
    y = y - h
    t.drawOn(p, x, y)

    # -- fin du pdf
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


def tableauPrescription(x, y, titre, info, prescription, p):
    h, w = A4
    otext = p.beginText()
    otext.setTextOrigin(x + 2 * mm, y)
    otext.setFont('Vera', 8)
    otext.textLine(titre)
    p.drawText(otext)

    sphere_od = NORM(prescription.sphere_od)
    cylindre_od = NORM(prescription.cylindre_od)
    if prescription.axe_od is not None:
        axe_od = str(prescription.axe_od) + " °"
    else:
        axe_od = ""
    addition_od = NORM(prescription.addition_od)

    sphere_og = NORM(prescription.sphere_og)
    cylindre_og = NORM(prescription.cylindre_og)
    if prescription.axe_og is not None:
        axe_og = str(prescription.axe_og) + " °"
    else:
        axe_og = ""
    addition_og = NORM(prescription.addition_og)

    datap = [[info, u"SPHERE", u"CYLINDRE", u"AXE", u"ADDITION"],
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
    t.drawOn(p, x, y - 16 * mm)


schu = ["", "UN ", "DEUX ", "TROIS ", "QUATRE ", "CINQ ", "SIX ", "SEPT ", "HUIT ", "NEUF "]
schud = ["DIX ", "ONZE ", "DOUZE ", "TREIZE ", "QUATORZE ", "QUINZE ", "SEIZE ", "DIX SEPT ", "DIX HUIT ", "DIX NEUF "]
schd = ["", "DIX ", "VINGT ", "TRENTE ", "QUARANTE ", "CINQUANTE ", "SOIXANTE ", "SOIXANTE ", "QUATRE VINGT ", "QUATRE VINGT "]


def n2l(nombre):
    s = ''
    reste = nombre
    i = 1000000000
    while i > 0:
        y = reste / i
        if y != 0:
            centaine = y / 100
            dizaine = (y - centaine * 100) / 10
            unite = y - centaine * 100 - dizaine * 10
            if centaine == 1:
                s += "CENT "
            elif centaine != 0:
                s += schu[centaine] + "CENT "
                if dizaine == 0 and unite == 0:
                    s = s[:-1] + "S "
            if dizaine not in [0, 1]:
                s += schd[dizaine]
            if unite == 0:
                if dizaine in [1, 7, 9]:
                    s += "DIX "
                elif dizaine == 8:
                    s = s[:-1] + "S "
            elif unite == 1:
                if dizaine in [1, 9]:
                    s += "ONZE "
                elif dizaine == 7:
                    s += "ET ONZE "
                elif dizaine in [2, 3, 4, 5, 6]:
                    s += "ET UN "
                elif dizaine in [0, 8]:
                    s += "UN "
            elif unite in [2, 3, 4, 5, 6, 7, 8, 9]:
                if dizaine in [1, 7, 9]:
                    s += schud[unite]
                else:
                    s += schu[unite]
            if i == 1000000000:
                if y > 1:
                    s += "MILLIARDS "
                else:
                    s += "MILLIARD "
            if i == 1000000:
                if y > 1:
                    s += "MILLIONS "
                else:
                    s += "MILLIONS "
            if i == 1000:
                s += "MILLE "
        #end if y!=0
        reste -= y * i
        dix = False
        i /= 1000
    #end while
    if len(s) == 0:
        s += "ZERO "
    return s
