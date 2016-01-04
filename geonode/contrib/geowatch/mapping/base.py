from geowatchutil.mapping.base import GeoWatchMapping

from django.conf import settings
# from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

# from geonode.base.models import Link

from geonode.contrib.geowatch.mapping.geowatch_mapping_layer import GeoWatchMappingLayer
from geonode.contrib.geowatch.mapping.geowatch_mapping_map import GeoWatchMappingMap
from geonode.contrib.geowatch.mapping.geowatch_mapping_document import GeoWatchMappingDocument
from geonode.contrib.geowatch.mapping.geowatch_mapping_user import GeoWatchMappingUser
from geonode.contrib.geowatch.mapping.geowatch_mapping_group import GeoWatchMappingGroup


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


def forward_layer(layer):
    mapping = GeoWatchMappingLayer()
    return mapping.forward(resource=layer)


def forward_map(map_obj):
    mapping = GeoWatchMappingMap()
    return mapping.forward(resource=map_obj)


def forward_document(document):
    mapping = GeoWatchMappingDocument()
    return mapping.forward(resource=document)


def forward_group(group):
    mapping = GeoWatchMappingGroup()
    return mapping.forward(group=group)


def forward_user(user):
    mapping = GeoWatchMappingUser()
    return mapping.forward(user=user)
