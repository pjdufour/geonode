from avatar.templatetags.avatar_tags import avatar_url

from django.conf import settings
from django.core.urlresolvers import reverse

from geonode.contrib.geowatch.mapping.base import GeoWatchMappingInstance


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
