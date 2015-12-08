from geowatchutil.mapping.base import GeoWatchMapping

from avatar.templatetags.avatar_tags import avatar_url

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from geonode.base.models import Link

class GeoWatchMappingInstance(GeoWatchMapping):

    def forward(self, **kwargs):
        site = Site.objects.get_current()
        message = {
            'sitename': site.name,
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
            'owner_name': (resource.owner.get_full_name() or resource.owner.username),
            'owner_url': owner_url,
            'thumbnail_url': thumbnail_url
        })
        return message

    def __init__(self):
        super(GeoWatchMappingResource, self).__init__()


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

        message['url_detail'] = url_detail
        message['url_shp'] = link_shp.url if link_shp else ''
        message['url_geojson'] = link_geojson.url if link_geojson else ''
        message['url_netkml'] = link_netkml.url if link_netkml else ''
        message['url_map'] = url_map

        return message

    def __init__(self):
        super(GeoWatchMappingLayer, self).__init__()


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

        message['url_detail'] = url_detail
        message['url_view'] = url_view
        message['url_download'] = url_download

        return message

    def __init__(self):
        super(GeoWatchMappingMap, self).__init__()


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
            'url_download': url_download
        })
        return message

    def __init__(self):
        super(GeoWatchMappingDocument, self).__init__()


class GeoWatchMappingGroup(GeoWatchMappingInstance):

    def forward(self, **kwargs):
        message = super(GeoWatchMappingGroup, self).forward(**kwargs)
        group = kwargs.get('group', None)

        thumbnail_url = group.logo.url if group.logo else ""
        url_detail = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('group_detail', args=(group.slug,)))

        message.update({
            'title': group.title,
            'type': 'group',
            'url_detail': url_detail,
            'thumbnail_url': thumbnail_url
        })
        return message

    def __init__(self):
        super(GeoWatchMappingGroup, self).__init__()


class GeoWatchMappingUser(GeoWatchMappingInstance):

    def forward(self, **kwargs):
        message = super(GeoWatchMappingUser, self).forward(**kwargs)
        user = kwargs.get('user', None)

        
        url_detail = "{base}{context}".format(
            base=settings.SITEURL[:-1],
            context=reverse('profile_detail', args=(user.username,)))

        message.update({
            'username': user.username,
            'type': 'user',
            'url_detail': url_detail,
            'thumbnail_url': avatar_url(user, 120),
            'access': 'admin' if user.is_superuser else ('staff' if user.is_staff else 'regular')
        })
        if message['access'] == 'admin':
            message['color'] = '#FF0000'
        else:
            message['color'] = '#0000FF'
        return message

    def __init__(self):
        super(GeoWatchMappingUser, self).__init__()


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
