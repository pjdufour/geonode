from django.conf import settings
from django.core.urlresolvers import reverse

from geonode.base.models import Link
from geonode.contrib.geowatch.mappings.base import GeoWatchMappingResource


class GeoWatchMappingLayer(GeoWatchMappingResource):

    def forward(self, **kwargs):
        message = super(GeoWatchMappingLayer, self).forward(**kwargs)
        layer = kwargs.get('resource', None)

        url_detail = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('layer_detail', args=(layer.service_typename,)))
        link_shp = Link.objects.get(resource=layer.get_self_resource(), name='Zipped Shapefile')
        link_geojson = Link.objects.get(resource=layer.get_self_resource(), name='GeoJSON')
        link_netkml = Link.objects.get(resource=layer.get_self_resource(), name='View in Google Earth')
        url_map = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse("new_map")+"?layer="+layer.service_typename)

        message.update({
            'service_typename': layer.service_typename,
            'url_detail': url_detail,
            'url_shp': link_shp.url if link_shp else '',
            'url_geojson': link_geojson.url if link_geojson else '',
            'url_netkml': link_netkml.url if link_netkml else '',
            'url_map': url_map
        })
        return message

    def __init__(self):
        super(GeoWatchMappingLayer, self).__init__()
