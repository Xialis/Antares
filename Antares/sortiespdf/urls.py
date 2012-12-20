from django.conf.urls import patterns, url

urlpatterns = patterns('sortiespdf.views',
        url(r'^fac/(?P<fid>\d+)/', 'facture'),
        )
