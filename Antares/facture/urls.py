from django.conf.urls import patterns, url

urlpatterns = patterns('facture.views',
        url(r'^$', 'index'),
        
        )
