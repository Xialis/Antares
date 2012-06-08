from django.conf.urls import patterns, url

urlpatterns = patterns('fournisseur.views',
        url(r'^$', 'index'),
        url(r'modType/(?P<tid>\d+)/$', 'modType', name="modType"),
        url(r'modTraitement/(?P<tid>\d+)/$', 'modTraitement', name="modTraitement"),
        url(r'modDiametre/(?P<did>\d+)/$', 'modDiametre', name="modDiametre"),
        url(r'modCouleur/(?P<cid>\d+)/$', 'modCouleur', name="modCouleur"),
        url(r'ajax_filtre_traitement/$', 'ajax_filtre_traitement', {}, 'ajax_filtre_traitement'),
        url(r'ajax_filtre_diametre/$', 'ajax_filtre_diametre', {}, 'ajax_filtre_diametre'),
        url(r'ajax_filtre_couleur/$', 'ajax_filtre_couleur', {}, 'ajax_filtre_couleur'),
        url(r'(?P<fid>\d+)/$', 'fournisseur', name="fournisseur"),

        )
