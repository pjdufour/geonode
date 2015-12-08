# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import json

from urlparse import urljoin

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from geonode.geoserver.helpers import ogc_server_settings
from geonode.layers.models import Layer
from geonode.services.models import Service
from geonode.utils import resolve_object

_PERMISSION_MSG_GENERIC = _('You do not have permissions for this layer.')
_PERMISSION_MSG_MODIFY = _("You are not permitted to modify this layer")


def _resolve_layer(request, typename, permission='base.view_resourcebase',
                   msg=_PERMISSION_MSG_GENERIC, **kwargs):
    """
    Resolve the layer by the provided typename (which may include service name) and check the optional permission.
    """
    service_typename = typename.split(":", 1)

    if Service.objects.filter(name=service_typename[0]).exists():
        service = Service.objects.filter(name=service_typename[0])
        return resolve_object(request,
                              Layer,
                              {'service': service[0],
                               'typename': service_typename[1] if service[0].method != "C" else typename},
                              permission=permission,
                              permission_msg=msg,
                              **kwargs)
    else:
        return resolve_object(request,
                              Layer,
                              {'typename': typename,
                               'service': None},
                              permission=permission,
                              permission_msg=msg,
                              **kwargs)


@login_required
def receive_layer_geojson(request, layername):
    layer = _resolve_layer(
        request,
        layername,
        'base.change_resourcebase',
        _PERMISSION_MSG_MODIFY)

    if request.method == "GET":
        return HttpResponse(
            "Must POST GeoJSON.",
            status=400,
            content_type="text/plain")

    elif request.method == "POST" or request.method == "PUT":

        data = json.loads(request.body)

        # WFS Insert Transaction
        ogc_wfs_path = '%s/wfs' % layer.workspace
        ogc_wfs_url = urljoin(ogc_server_settings.public_url, ogc_wfs_path)

        #from geowatchutil.runtime import provision_producer
        #client, producer = provision_producer(
        #    "wfs",
        #    topic=layer.typename,
        #    codec="wfs",
        #    url=ogc_wfs_url)
        #response = producer.send_message(data, cookie=request.META['HTTP_COOKIE'])

        from geowatchutil.runtime import provision_store
        store = provision_store(
            "wfs",
            layer.typename,
            "wfs",
            url=ogc_wfs_url)
        response = store.write_message(data, flush=True, flush_kwargs={'cookie': request.META['HTTP_COOKIE']})
        print "Response: ", response.read()

        return HttpResponse(
            response,
            status=400,
            content_type="appplication/json")
