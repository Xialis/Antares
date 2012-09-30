from django.conf.urls import patterns, url

urlpatterns = patterns('facture',
        url(r'^$', 'func.ctrl'),
        url(r'^creerClient/', 'func.creerClient'),
        url(r'^utiliserClient/(?P<cid>\d+)/', 'func.utiliserClient'),
        url(r'^etapeSuivante/', 'func.etapeSuivante'),
        url(r'^etapePrecedente/', 'func.etapePrecedente'),
        url(r'^etape/(?P<etape>\d+)/', 'func.allerEtape'),
        url(r'ajax_filtre/$', 'views.ajax_filtre', {}, 'ajax_filtre'),
        url(r'ajax_info/$', 'views.ajax_info', {}, 'ajax_info'),
        url(r'^reset', 'func.reset'),
        )
