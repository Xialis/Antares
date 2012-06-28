# -*- coding: utf-8 -*-


def app_context(request):
    appClient = {}

    if 'appClient' in request.session:
        s_appClient = request.session['appClient']

        if 'filtrage' in s_appClient:
            appClient.update({'b_listeFiltree': True})

    return {'appClient': appClient}
