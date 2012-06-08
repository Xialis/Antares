from django.conf.urls import patterns, url

urlpatterns = patterns('stock.views',
        url(r'^$', 'index'),
        url(r'^(?P<fid>\d+)/', 'gestionStock'),
        )
