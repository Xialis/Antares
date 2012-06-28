# -*- coding: utf-8 -*-


def app_context(request):
    appFacture = {}
    
    if 'appFacture' in request.session:
        s_appFacture = request.session['appFacture']

    return {'appFacture': appFacture}
