from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from guardian.shortcuts import get_users_with_perms, get_perms, remove_perm, assign_perm

try:
    import simplejson as json
except ImportError:
    import json

from geodash.utils import extract

from geonode.layers.models import Layer
from geonode.maps.models import Map, MapLayer
from geonode.people.models import Profile
from geonode.utils import resolve_object

def expand_users(request, map_obj):
    users = []
    if request.user.has_perm("change_geodashdashboard", map_obj):
        users =[{'id': x.username, 'text': x.username} for x in Profile.objects.exclude(username='AnonymousUser')]
    return users


def expand_perms(map_obj):
    allperms = get_users_with_perms(map_obj, attach_perms=True)
    return {
        "advertised": map_obj.advertised,
        "published": map_obj.published,
        'view_dashboard': sorted([x.username for x in allperms if 'view_dashboard' in allperms[x]]),
        'change_dashboard': sorted([x.username for x in allperms if 'change_dashboard' in allperms[x]]),
        'delete_dashboard': sorted([x.username for x in allperms if 'delete_dashboard' in allperms[x]])
    }


def build_servers():
    data = []
    OGC_SERVER = getattr(settings, "OGC_SERVER")
    if OGC_SERVER:
        site = Site.objects.get_current()
        title = (site.name + " (OGC Server)") if site.name else "Local OGC Server"
        public_location = extract("default.PUBLIC_LOCATION", OGC_SERVER, None)
        if public_location:
            server = {
              "id": "local",
              "title": title,
              "description": "Local OGC Server",
              "type": "wms",
              "wms": {
                  "url": public_location + "wms"
              },
              "wfs": {
                  "version": "1.0.0",
                  "url": public_location +"wfs"
              }
            }

        if server:
            data.append(server)

    return data


def build_baselayers():
    data = []
    MAP_BASELAYERS = getattr(settings, 'MAP_BASELAYERS', None)
    if MAP_BASELAYERS:
        for x in MAP_BASELAYERS:
            bl = None
            sourceType = extract('source.ptype', x, None)
            if sourceType:
                if sourceType == "gxp_osmsource":
                    bl = {
                      "id": "osm",
                      "title": "OpenStreetMap",
                      "description": "OpenStreetMap Basemap, Standard Style",
                      "type": "tiles",
                      "source": {
                        "name": "OpenStreetMap",
                        "attribution": "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a>"
                      },
                      "tile": {
                          "url": "https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      }
                    }
                elif sourceType == "gxp_mapboxsource":
                    access_token = getattr(settings, "MAPBOX_ACCESS_TOKEN", None)
                    name = extract("name", x)
                    bl = {
                      "id": name,
                      "title": extract("title", x),
                      "description": "",
                      "type": "mapbox",
                      "source": {},
                      "mapbox": {
                          "layer": "mapbox."+name,
                          "access_token": access_token
                      }
                    }
                elif sourceType == "gxp_olsource":
                    name = extract("name", x, None)
                    args = extract("args", x, None)
                    if args:
                        url = extract([1, 0], args, None) if len(args) >= 2 else None
                        if url:
                            for i in ['x', 'y', 'z']:
                                url = url.replace("${"+i+"}", "{"+i+"}")
                            url = url.replace("a.tile.openstreetmap.fr", "{a-c}.tile.openstreetmap.fr")
                            bl = {
                              "id": name,
                              "title": extract(["args", 0], x, None),
                              "description": "",
                              "type": "tiles",
                              "source": {},
                              "tile": {
                                  "url": url
                              }
                            }

            if bl:
              data.append(bl)

    return data

def build_featurelayers(request=None, layers=None, map_obj=None):
    data = []
    if map_obj:
        layers = MapLayer.objects.filter(map=map_obj.id)
        for layer in layers:
            ows_url = layer.ows_url
            if ows_url:
                public_location = layer.ows_url[:-3]
                GEODASH_OGC_SERVER_PORT = getattr(settings, "GEODASH_OGC_SERVER_PORT", 8080)
                if GEODASH_OGC_SERVER_PORT:
                    public_location = public_location.replace("8080", str(GEODASH_OGC_SERVER_PORT))
                layer_params = json.loads(layer.layer_params)
                fields = []

                localLayer = None
                if layer.local:
                    #try:
                    localLayer = resolve_object(
                        request,
                        Layer,
                        {'typename': layer.name, 'service': None},
                        permission='base.view_resourcebase',
                        permission_msg=_("You are not permitted to view this layer")
                    )
                    #except:
                    #    pass

                if localLayer:
                    print "Local Layer:", localLayer
                    for attribute in localLayer.attributes.filter(display_order__gte=1).order_by("display_order"):
                        fields.append({
                            "attribute": attribute.attribute,
                            "label": attribute.attribute_label or attribute.attribute,
                            "value": "{{ feature.attributes."+attribute.attribute+" }}"
                        })

                fields.append({
                "type": "link",
                "value": "OpenStreetMap",
                "url": "https://www.openstreetmap.org/#map=15/{{ feature.geometry.lat | number : 4 }}/{{ feature.geometry.lon | number : 4 }}"
                })

                fl = {
                  "id": layer.id,
                  "title": layer_params.get('title', layer.id),
                  "description": extract('capability.abstract', layer_params, ''),
                  "type": "wms",
                  "wms": {
                      "url": public_location + "wms",
                      "layers": [extract('capability.name', layer_params, layer.name)],
                      "styles": "",
                      "buffer": 256,
                      "version": "1.1.1",
                      "format": "image/png",
                      "transparent": True
                  },
                  "wfs": {
                      "version": "1.0.0",
                      "url": public_location +"wfs",
                      "layers": [extract('capability.name', layer_params, layer.name)]
                  },
                  "popup": {
                      "title": extract('title', layer_params, layer.name),
                      "css": {
                          "properties": [
                              { "name": "max-width", "value": "550px" },
                              { "name": "min-width", "value": "220px" }
                          ]
                      },
                      "panes": [{
                          "id": "popup_overview",
                          "tab": {
                              "label": "Overview"
                          },
                          "fields": fields
                      }]
                  }
                }

                if fl:
                    data.append(fl)

    elif layers:
        OGC_SERVER = getattr(settings, "OGC_SERVER")
        if OGC_SERVER:
            public_location = extract("default.PUBLIC_LOCATION", OGC_SERVER, None)
            if public_location:
                GEODASH_OGC_SERVER_PORT = getattr(settings, "GEODASH_OGC_SERVER_PORT", 8080)
                if GEODASH_OGC_SERVER_PORT:
                    public_location = public_location.replace("8080", str(GEODASH_OGC_SERVER_PORT))
                for layer in layers:

                    fields = []
                    for attribute in layer.attributes.filter(display_order__gte=1).order_by("display_order"):
                        fields.append({
                            "attribute": attribute.attribute,
                            "label": attribute.attribute_label or attribute.attribute,
                            "value": "{{ feature.attributes."+attribute.attribute+" }}"
                        })

                    fields.append({
                      "type": "link",
                      "value": "OpenStreetMap",
                      "url": "https://www.openstreetmap.org/#map=15/{{ feature.geometry.lat | number : 4 }}/{{ feature.geometry.lon | number : 4 }}"
                    })

                    fl = {
                      "id": layer.uuid,
                      "title": layer.title,
                      "description": layer.abstract,
                      "type": "wms",
                      "wms": {
                          "url": public_location + "wms",
                          "layers": [layer.typename],
                          "styles": "",
                          "buffer": 256,
                          "version": "1.1.1",
                          "format": "image/png",
                          "transparent": True
                      },
                      "wfs": {
                          "version": "1.0.0",
                          "url": public_location +"wfs",
                          "layers": [layer.typename]
                      },
                      "popup": {
                          "title": layer.title,
                          "css": {
                              "properties": [
                                  { "name": "max-width", "value": "550px" },
                                  { "name": "min-width", "value": "220px" }
                              ]
                          },
                          "panes": [{
                              "id": "popup_overview",
                              "tab": {
                                  "label": "Overview"
                              },
                              "fields": fields
                          }]
                      }
                    }

                    if fl:
                        data.append(fl)

    return data
