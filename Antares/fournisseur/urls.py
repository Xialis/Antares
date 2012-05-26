from django.conf.urls import patterns, url

urlpatterns = patterns('fournisseur.views',
        url(r'^$', 'index'),
        url(r'modType/(?P<tid>\d+)/$', 'modType', name="modType"),
        url(r'modTraitement/(?P<tid>\d+)/$', 'modTraitement', name="modTraitement"),
        url(r'(?P<fid>\d+)/$', 'fournisseur', name="fournisseur"),

        )
