from django.conf.urls import patterns, include, url
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'Antares.views.home', name='home'),
    # url(r'^Antares/', include('Antares.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'fournisseur/', include('fournisseur.urls')),
    url(r'stock/', include('stock.urls')),
    url(r'client/', include('client.urls')),
    url(r'facture/', include('facture.urls')),
    url(r'commande/', include('commande.urls')),
    url(r'sortiespdf/', include('sortiespdf.urls')),
)
