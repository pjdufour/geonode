from django.conf import settings
from django.core.urlresolvers import reverse

from geonode.contrib.geowatch.mapping.base import GeoWatchMappingResource


class GeoWatchMappingMap(GeoWatchMappingResource):

    def forward(self, **kwargs):
        message = super(GeoWatchMappingMap, self).forward(**kwargs)
        map_obj = kwargs.get('resource', None)

        url_detail = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('map_detail', args=(map_obj.id,)))
        url_view = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('map_view', args=(map_obj.id,)))
        url_download = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('map_download', args=(map_obj.id,)))

        message.update({
            'url_detail': url_detail,
            'url_view': url_view,
            'url_download': url_download,
            'id': map_obj.id
        })
        return message

    def __init__(self):
        super(GeoWatchMappingMap, self).__init__()
