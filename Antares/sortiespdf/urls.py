from django.conf.urls import patterns, url

urlpatterns = patterns('sortiespdf',
        url(r'^fac/(?P<fid>\d+)/', 'views.facture'),
        url(r'^com/(?P<cid>\d+)/', 'genPDFcommande.commandepdf'),
        )
