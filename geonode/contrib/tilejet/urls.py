from django.conf.urls import patterns

urlpatterns = patterns('geonode.contrib.tilejet.views', (r'^proxy/', 'proxy'),)
