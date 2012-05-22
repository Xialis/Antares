from django.conf.urls import patterns, include, url

urlpatterns = patterns('fournisseur.views',
        url(r'^$', 'index'),
        url(r'(?P<fid>\d+)/$', 'fournisseur', name="fournisseur"),
        )
