from django.conf.urls import patterns, url

urlpatterns = patterns('client.views',
        url(r'^$', 'index'),
        url(r'^(?P<cid>\d+)/', 'infoClient'),
        url(r'^ajaxClientList/', 'ajaxListClient'),
        )
