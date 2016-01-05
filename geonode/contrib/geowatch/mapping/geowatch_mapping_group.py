from django.conf import settings
from django.core.urlresolvers import reverse

from geonode.contrib.geowatch.mapping.base import GeoWatchMappingInstance


class GeoWatchMappingGroup(GeoWatchMappingInstance):

    def forward(self, **kwargs):
        message = super(GeoWatchMappingGroup, self).forward(**kwargs)
        group = kwargs.get('group', None)

        thumbnail_url = group.logo.url if group.logo else ""
        url_detail = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('group_detail', args=(group.slug,)))

        message.update({
            'slug': group.slug,
            'title': group.title,
            'type': 'group',
            'url_detail': url_detail,
            'thumbnail_url': thumbnail_url
        })
        return message

    def __init__(self):
        super(GeoWatchMappingGroup, self).__init__()
