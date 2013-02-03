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
from commande.models import Commande

import os
APP_ROOT = os.path.dirname(os.path.realpath(__file__))


def commande(request, cid):

    commande = Commande.objects.get(id=cid)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="com.' + commande.fournisseur.nom + '.' + commande.numero + '.pdf"'

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
    
    data = [["Info", "Type", "Couleur", "Traitement", "Diametre", "Sphere", "Cylindre", "Axe", "Addition", "Qte", "Qte Reçu"],
            ]
    
    for lc in commande:
        line = []

        if lc.ligne_facture is None:
            # Info
            line.append("Stock")
            req = lc.ligne_stock
        else:
            line.append(lc.ligne_facture.client.nom + " " + lc.ligne_facture.client.prenom)
            req = lc.ligne_facture

        # Type
        line.append(req.vtype.nom)

        # Couleur
        line.append(req.couleur.nom)

        # Traitement
        line.append(req.traitement.nom)

        # Diametre
        line.append(req.diametre.nom)

        # sphere
        line.append(NORM(req.sphere))

        # cylindre
        line.append(NORM(req.cylindre))
        
        # axe
        if lc.ligne_facture is not None:
            line.append(req.axe)
        
        # Addition
        if lc.ligne_facture is not None:
            line.append(req.addition)
        
        # Qte
        line.append(lc.quantite)

        # Qte Reçu
        line.append(lc.quantite_recu)

        data.append(line)