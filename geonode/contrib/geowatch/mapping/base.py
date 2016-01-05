from geowatchutil.mapping.base import GeoWatchMapping

from django.conf import settings
# from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

# from geonode.base.models import Link


class GeoWatchMappingInstance(GeoWatchMapping):

    def forward(self, **kwargs):
        site = Site.objects.get_current()
        message = {
            'site_name': site.name,
            'baseurl': settings.SITEURL
        }
        return message

    def __init__(self):
        super(GeoWatchMappingInstance, self).__init__()


class GeoWatchMappingResource(GeoWatchMappingInstance):

    def forward(self, **kwargs):
        message = super(GeoWatchMappingResource, self).forward(**kwargs)
        resource = kwargs.get('resource', None)

        thumbnail_url = resource.get_thumbnail_url()
        owner_url = "{base}{context}".format(base=settings.SITEURL[:-1], context=resource.owner.get_absolute_url())

        message.update({
            'title': resource.title,
            'type': str(resource.polymorphic_ctype),
            'owner_username': resource.owner.username,
            'owner_name': (resource.owner.get_full_name() or resource.owner.username),
            'owner_url': owner_url,
            'thumbnail_url': thumbnail_url
        })
        return message

    def __init__(self):
        super(GeoWatchMappingResource, self).__init__()
