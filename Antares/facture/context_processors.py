# -*- coding: utf-8 -*-
from client.models import Client


def app_context(request):
    appFacture = {}

    if 'appFacture' in request.session:
        s_appFacture = request.session['appFacture']

        if 'etapes' in s_appFacture:
            etapes = []
            for etape in s_appFacture['etapes']:
                etapes.append(etape[0])
            appFacture.update({'etapes': etapes})
            appFacture.update({'etape_no': s_appFacture['etape'] + 1})

        if 'b_creation' in s_appFacture:
            appFacture.update({'b_creation': s_appFacture['b_creation']})

        if 'b_modification' in s_appFacture:
            appFacture.update({'b_modification': s_appFacture['b_modification']})

        if 'client_id' in s_appFacture:
            appFacture.update({'client_id': s_appFacture['client_id']})
            client = Client.objects.get(id=s_appFacture['client_id'])
            appFacture.update({'client': client})

        if 'client' in s_appFacture:
            client = s_appFacture['client']
            appFacture.update({'client': client})

        if 'progressif_od' in s_appFacture:
            if s_appFacture['progressif_od'] == True:
                appFacture.update({'progressif_od': 'p'})
            else:
                appFacture.update({'progressif_od': 'u'})
        else:
            appFacture.update({'progressif_od': None})

        if 'progressif_og' in s_appFacture:
            if s_appFacture['progressif_og'] == True:
                appFacture.update({'progressif_og': 'p'})
            else:
                appFacture.update({'progressif_og': 'u'})
        else:
            appFacture.update({'progressif_og': None})

        if 'prescription' in s_appFacture:
            p = s_appFacture['prescription']
            if abs(p.sphere_od) > 4 or abs(p.sphere_og) > 4:
                appFacture.update({'attention_sphere': True})

        if 'prescription_sphod' in s_appFacture:
            sod = s_appFacture['prescription_sphod']
            sog = s_appFacture['prescription_sphog']

            appFacture.update({'sphod': sod})
            appFacture.update({'sphog': sog})

        if 'prescription_t' in s_appFacture:
            axe_od = s_appFacture['prescription_t'].axe_od
            if  axe_od is None:
                axe_od = 0

            axe_og = s_appFacture['prescription_t'].axe_og
            if  axe_og is None:
                axe_og = 0

            if abs(axe_od - axe_og) > 90:
                contraxe = True
            else:
                contraxe = False

            cyl_od = s_appFacture['prescription_t'].cylindre_od
            cyl_og = s_appFacture['prescription_t'].cylindre_og

            if cyl_od is not None and cyl_od != 0:
                bod = True
            else:
                bod = False

            if cyl_og is not None and cyl_og != 0:
                bog = True
            else:
                bog = False

            appFacture.update({'astig_od': bod})
            appFacture.update({'astig_og': bog})
            appFacture.update({'contraxe': contraxe})

    return {'appFacture': appFacture}
