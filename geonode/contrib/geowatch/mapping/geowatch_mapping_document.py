from django.conf import settings
from django.core.urlresolvers import reverse

from geonode.contrib.geowatch.mappings.base import GeoWatchMappingResource


class GeoWatchMappingDocument(GeoWatchMappingResource):

    def forward(self, **kwargs):
        message = super(GeoWatchMappingDocument, self).forward(**kwargs)
        document = kwargs.get('resource', None)

        url_detail = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('document_detail', args=(document.id,)))
        url_download = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('document_download', args=(document.id,)))

        message.update({
            'url_detail': url_detail,
            'url_download': url_download,
            'id': document.id
        })
        return message

    def __init__(self):
        super(GeoWatchMappingDocument, self).__init__()
