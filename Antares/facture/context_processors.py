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

    return {'appFacture': appFacture}
