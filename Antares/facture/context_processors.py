# -*- coding: utf-8 -*-


def app_context(request):
    appFacture = {}

    if 'appFacture' in request.session:
        s_appFacture = request.session['appFacture']

        if 'etapes' in s_appFacture:
            etapes = []
            for etape in s_appFacture['etapes']:
                etapes.append(etape[0])
            appFacture.update({'etapes': etapes})

    return {'appFacture': appFacture}
