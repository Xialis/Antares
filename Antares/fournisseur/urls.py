from django.conf.urls import patterns, include, url

urlpatterns = patterns('fournisseur.views',
        url(r'^$', 'index'),
        url(r'modType/(?P<tid>\d+)/$', 'modType', name="modType"),
        url(r'(?P<fid>\d+)/$', 'fournisseur', name="fournisseur"),
        
        )
