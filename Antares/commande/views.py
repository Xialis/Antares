# -*- coding: utf-8 -*-

# import Django
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import messages
from django.core.context_processors import csrf
from django.forms.formsets import formset_factory

# import Antares
from fournisseur.models import Fournisseur
from commande.models import Commande, LigneCommande
from commande.forms import ComRecepForm
from stock.func import modstock
import func


def index(request):
    c = {}

    listeFournisseur = Fournisseur.objects.all()

    c['listeFournisseur'] = listeFournisseur
    c.update(csrf(request))
    return render_to_response("commande/index.html", c, context_instance=RequestContext(request))


def commandesF(request, fid):
    c = {}
    fournisseur = Fournisseur.objects.get(id=fid)

    # == Traitement POST
    if request.method == 'POST':

        form = ComRecepForm(request.POST)
        if form.is_valid():
            lID = form.cleaned_data['lignecommande_id']
            qte_recu = form.cleaned_data['recu']
            lc = LigneCommande.objects.get(id=lID)
            lc.quantite_recu = lc.quantite_recu + qte_recu
            lc.save()
            messages.add_message(request, messages.SUCCESS, u"Verre(s) reçu(s) validé(s)")
            if lc.ligne_stock is not None:
                retour = modstock(lc.ligne_stock, qte_recu)
                if retour == True:
                    messages.add_message(request, messages.SUCCESS, u"Modification du stock avec verre(s) reçu(s)")
            else:
                messages.add_message(request, messages.SUCCESS, u"Verre(s) de prescription reçu !")

            return redirect(reverse(commandesF, kwargs={'fid': fournisseur.id}) + "#com" + str(lc.id))
        else:
            messages.add_message(request, messages.ERROR, u"Erreur de saisie !")

    # ==

    listeCommandes = Commande.objects.filter(fournisseur=fournisseur).order_by('-id')
    cid = listeCommandes[0].id
    comRecepForm = ComRecepForm()

    # gestion commande stock
    liste = func.listeStock(fournisseur)

    c['liste'] = liste
    c['listeCommandes'] = listeCommandes
    c['cid'] = cid
    c['comRecepForm'] = comRecepForm
    c.update(csrf(request))
    return render_to_response("commande/commandesF.html", c, context_instance=RequestContext(request))


def validationCommande(request, cid):
    commande = Commande.objects.get(id=cid)
    if func.validerCommande(commande):
        messages.add_message(request, messages.SUCCESS, u"Commande validée")
        func.nouvelleCommande(commande.fournisseur)
    else:
        messages.add_message(request, messages.ERROR, u"Erreur de validation, rien à commander !")

    return redirect(commandesF, fid=commande.fournisseur.id)

