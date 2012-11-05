from django.conf.urls import patterns, url

urlpatterns = patterns('commande.views',
        url(r'^$', 'index'),
        url(r'f/(?P<fid>\d+)/$', 'commandesF'),
        url(r'validation/(?P<cid>\d+)/$', 'validationCommande'),
        )
