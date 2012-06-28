from django.conf.urls import patterns, url

urlpatterns = patterns('facture',
        url(r'^$', 'views.index'),
        url(r'^creerClient/', 'func.creerClient'),
        url(r'^utiliserClient/(?P<cid>\d+)/', 'func.utiliserClient'),
        url(r'^etapeSuivante/', 'func.etapeSuivante'),
        url(r'^etapePrecedente/', 'func.etapePrecedente'),
        url(r'^etape/(?P<etape>\d+)/', 'func.allerEtape'),
        )
