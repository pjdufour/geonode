from account.models import EmailAddress

from geowatchutil.base import GeoWatchError
from geowatchutil.broker.base import GeoWatchBroker

# from django.conf import settings
# from django.core.mail import send_mail
# from django.core.mail import EmailMultiAlternatives
# from django.shortcuts import get_object_or_404
# from django.template import Context, Template
from django.template.loader import get_template

from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.people.models import Profile
from geonode.groups.models import GroupProfile


class GeoNodeBroker(GeoWatchBroker):
    """
    Base class for GeoNode brokers.  Implements a few utility functions.
    """

    def _pre(self):
        pass

    def _post(self):
        pass

    def _get_owner(self, data):
        user = None
        try:
            user = Profile.objects.get(username=data[u'owner_username'])
        except:
            print "Could not find owner"
            user = None
        return user

    def _get_email(self, user):
        email = None
        try:
            email = EmailAddress.objects.filter(user=user, primary=True, verified=True)[0]
        except:
            print "Could not get email for user"+user.username
        return email

    def _get_instance(self, data):
        if data[u'type'] == u'layer':
            return self._get_layer(data)
        elif data[u'type'] == u'map':
            return self._get_map(data)
        elif data[u'type'] == u'document':
            return self._get_document(data)
        elif data[u'type'] == u'group':
            return self._get_group(data)
        else:
            return None

    def _get_layer(self, data):
        layer = None
        try:
            layer = Layer.objects.get(typename=data[u'service_typename'], service=None).get_self_resource()
        except:
            print "Could not find layer"
            layer = None
        return layer

    def _get_map(self, data):
        map_obj = None
        try:
            map_obj = Map.objects.get(id=data[u'id']).get_self_resource()
        except:
            print "Could not find map"
            map_obj = None
        return map_obj

    def _get_document(self, data):
        document = None
        try:
            document = Document.objects.get(id=data[u'id']).get_self_resource()
        except:
            print "Could not find document"
            document = None
        return document

    def _get_group(self, data):
        group = None
        try:
            group = GroupProfile.objects.get(slug=data[u'slug']).get_self_resource()
        except:
            print "Could not find group"
            group = None
        return group

    def _render_template(self, context=None, template=None):
        if context and template:
            return get_template(template).render(context)
        else:
            raise GeoWatchError("Could not render template "+str(template))
