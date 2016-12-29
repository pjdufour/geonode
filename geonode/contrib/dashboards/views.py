import datetime
import requests
import yaml
import errno
from socket import error as socket_error
from pyproj import transform, Proj

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import ugettext as _

#from guardian.models import UserObjectPermission
from guardian.shortcuts import get_users_with_perms, get_perms, remove_perm, assign_perm

try:
    import simplejson as json
except ImportError:
    import json

from geonode.layers.models import Layer, Attribute, UploadSession
from geonode.maps.models import Map
from geonode.people.models import Profile
from geonode.utils import resolve_object

from geodash.cache import provision_memcached_client
from geodash.utils import build_state_schema, build_context, build_editor_config, build_dashboard_config
from geodash.security import check_perms_view, geodash_assign_default_perms
from geodash.views import GeoDashDictWriter

from geonode.contrib.dashboards.enumerations import ENDPOINTS, PAGES
from geonode.contrib.dashboards.models import Dashboard
from geonode.contrib.dashboards.utils import expand_users, expand_perms, build_baselayers, build_featurelayers, build_servers

SCHEMA_PATH = 'geonode/contrib/dashboards/static/dashboards/build/schema/schema.yml'


def _build_response(request, data, extension):

    ext_lc = extension.lower();
    if ext_lc == "json":
        return HttpResponse(json.dumps(data), content_type="application/json")
    elif ext_lc == "yml" or ext_lc == "yaml":
        response = yaml.safe_dump(data, encoding="utf-8", allow_unicode=True, default_flow_style=False)
        return HttpResponse(response, content_type="text/plain")
    else:
        raise Http404("Unknown config format.")


def dashboards_browse(request, template="dashboards/browse.html"):
    now = datetime.datetime.now()
    current_month = now.month

    longitude, latitude = getattr(settings, 'DEFAULT_MAP_CENTER', (0, 0));
    zoom = getattr(settings, 'DEFAULT_MAP_ZOOM', 3)
    config = yaml.load(get_template("dashboards/browse/config.yml").render({
        "latitude": latitude,
        "longitude": longitude,
        "zoom": zoom
    }))

    dashboard_resources = [
        { "loader": "endpoints", "url": reverse("dashboards_api_endpoints", kwargs={"extension": "json"}) },
        { "loader": "pages", "url": reverse("dashboards_api_pages", kwargs={"extension": "json"}) }
    ];

    ctx = {
        "dashboard_url": reverse("dashboards_api_config", kwargs={"type": "dashboard", "uuid": "browse", "extension": "json"}),
        "state_url": reverse("dashboards_api_state", kwargs={"type": "dashboard", "uuid": "browse", "extension": "json"}),
        "state_schema_url": reverse("dashboards_api_schema", kwargs={"name": "state", "extension": "json"}),
        "geodash_main_id": "geodash-main",
        "include_sidebar_left": False,
        "include_sidebar_left": False,
        "modal_welcome": True
    }

    ctx.update({
      "dashboard_resources_json": json.dumps(dashboard_resources)
    })

    ctx.update({
      "server_templates": json.dumps({
          "main.tpl.html": get_template("dashboards/browse/main.tpl.html").render(ctx)
      })
    })

    return render_to_response(template, RequestContext(request, ctx))


def dashboards_page(request, uuid=None, template="dashboards/dashboard.html"):

    map_obj = get_object_or_404(Dashboard, uuid=uuid)

    check_perms_view(request, map_obj, raiseErrors=True)

    config = build_dashboard_config(map_obj)
    config_schema = yaml.load(file(SCHEMA_PATH,'r'))

    #editor_template = "geodash/editor/editor.yml"
    #editor_yml = get_template(eildditor_template).render({})
    #editor = yaml.load(editor_yml)

    #security = expand_perms(map_obj)

    #ctx = build_context(
    #    config,
    #    build_initial_state(config, page="dashboard", slug=uuid),
    #    build_state_schema())
    #ctx = build_context(config, {}, build_state_schema);

    #ctx = {
    #    "dashboards": dashboards,
    #    "dashboards_json": json.dumps(dashboards),
        #"state": initial_state,
        #"state_json": json.dumps(initial_state),
    #    "state_schema": state_schema,
    #    "state_schema_json": json.dumps(state_schema),
    #    "init_function": "init.dashboard",
    #    "geodash_main_id": "geodash-main"
    #}

    #ctx.update({
        #"pages_json": json.dumps(pages),
    #    "map_config_schema": config_schema,
    #    "map_config_schema_json": json.dumps(config_schema),
    #    "editor": editor,
    #    "editor_json": json.dumps(editor),
    #    "security": security,
    #    "security_json": json.dumps(security),
    #    "security_schema": security_schema,
    #    "security_schema_json": json.dumps(security_schema),
    #    "include_sidebar_right": request.user.has_perm("change_dashboard", map_obj),
    #    "perms_json": json.dumps(get_perms(request.user, map_obj)),
    #    "users": json.dumps(expand_users(request, map_obj))
    #})

    dashboard_resources = [
        { "name": "security", "url": reverse("dashboards_api_security", kwargs={"type": "dashboard", "uuid": uuid, "extension": "json"}) },
        { "loader": "endpoints", "url": reverse("dashboards_api_endpoints", kwargs={"extension": "json"}) },
        { "loader": "pages", "url": reverse("dashboards_api_pages", kwargs={"extension": "json"}) },
        { "name": "dashboard_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "config", "extension": "json"})},
        { "name": "editor_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "editor", "extension": "json"})},
        { "name": "security_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "security", "extension": "json"})}
    ];

    ctx = {
        "dashboard": config, # needed for Django templates
        "dashboard_url": reverse("dashboards_api_config", kwargs={"type": "dashboard", "uuid": uuid, "extension": "json"}),
        "state_url": reverse("dashboards_api_state", kwargs={"type": "dashboard", "uuid": uuid, "extension": "json"}),
        "state_schema_url": reverse("dashboards_api_schema", kwargs={"name": "state", "extension": "json"}),
        "geodash_main_id": "geodash-main",
        "include_sidebar_left": False,
        "include_sidebar_left": False,
        "modal_welcome": True
    }

    ctx.update({
      "dashboard_resources_json": json.dumps(dashboard_resources)
    })

    ctx.update({
      "server_templates": json.dumps({
          "main.tpl.html": get_template("dashboards/editor/main.tpl.html").render(ctx)
      })
    })

    return render_to_response(template, RequestContext(request, ctx))


def dashboards_new(request, type=None, uuid=None, template="dashboards/dashboard.html"):

    if type == "map":

        dashboard_resources = [
            { "name": "security", "url": reverse("dashboards_api_security", kwargs={"type": "map", "uuid": uuid, "extension": "json"}) },
            { "loader": "endpoints", "url": reverse("dashboards_api_endpoints", kwargs={"extension": "json"}) },
            { "loader": "pages", "url": reverse("dashboards_api_pages", kwargs={"extension": "json"}) },
            { "name": "dashboard_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "config", "extension": "json"})},
            { "name": "editor_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "editor", "extension": "json"})},
            { "name": "security_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "security", "extension": "json"})}
        ];

        ctx = {
            "dashboard_url": reverse("dashboards_api_config", kwargs={"type": "map", "uuid": uuid, "extension": "json"}),
            "state_url": reverse("dashboards_api_state", kwargs={"type": "map", "uuid": uuid, "extension": "json"}),
            "state_schema_url": reverse("dashboards_api_schema", kwargs={"name": "state", "extension": "json"}),
            "geodash_main_id": "geodash-main",
            "include_sidebar_left": False,
            "include_sidebar_left": False,
            "modal_welcome": True,
            "dashboard_resources_json": json.dumps(dashboard_resources)
        }

        ctx.update({
            "server_templates": json.dumps({
                "main.tpl.html": get_template("dashboards/editor/main.tpl.html").render(ctx)
            })
        })

        return render_to_response(template, RequestContext(request, ctx))

    elif type == "layer":

        dashboard_resources = [
            { "name": "security", "url": reverse("dashboards_api_security", kwargs={"type": "layer", "uuid": uuid, "extension": "json"}) },
            { "loader": "endpoints", "url": reverse("dashboards_api_endpoints", kwargs={"extension": "json"}) },
            { "loader": "pages", "url": reverse("dashboards_api_pages", kwargs={"extension": "json"}) },
            { "name": "dashboard_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "config", "extension": "json"})},
            { "name": "editor_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "editor", "extension": "json"})},
            { "name": "security_schema", "url": reverse("dashboards_api_schema", kwargs={"name": "security", "extension": "json"})}
        ];

        ctx = {
            "dashboard_url": reverse("dashboards_api_config", kwargs={"type": "layer", "uuid": uuid, "extension": "json"}),
            "state_url": reverse("dashboards_api_state", kwargs={"type": "layer", "uuid": uuid, "extension": "json"}),
            "state_schema_url": reverse("dashboards_api_schema", kwargs={"name": "state", "extension": "json"}),
            "geodash_main_id": "geodash-main",
            "include_sidebar_left": False,
            "include_sidebar_left": False,
            "modal_welcome": True,
            "dashboard_resources_json": json.dumps(dashboard_resources)
        }

        ctx.update({
            "server_templates": json.dumps({
                "main.tpl.html": get_template("dashboards/editor/main.tpl.html").render(ctx)
            })
        })

        return render_to_response(template, RequestContext(request, ctx))

    else:
        return None


def dashboards_api_config(request, type=None, uuid=None, extension="json"):
    if type == "dashboard":
        if uuid == "browse":
            longitude, latitude = getattr(settings, 'DEFAULT_MAP_CENTER', (0, 0));
            zoom = getattr(settings, 'DEFAULT_MAP_ZOOM', 3)
            site = site = Site.objects.get_current()
            config = yaml.load(get_template("dashboards/browse/config.yml").render({
                "SITE_NAME": site.name,
                "SITE_DOMAIN": site.domain,
                "latitude": latitude,
                "longitude": longitude,
                "zoom": zoom
            }))
            config['slug'] = uuid
            config['baselayers'] = build_baselayers()
            config['servers'] = build_servers()
            return _build_response(request, config, extension)

        else:
            map_obj = get_object_or_404(Dashboard, uuid=uuid)
            check_perms_view(request, map_obj, raiseErrors=True)
            config = yaml.load(map_obj.config)
            config["slug"] = map_obj.uuid
            config["title"]  = map_obj.title
            return _build_response(request, config, extension)

    elif type == "map":

        map_obj = resolve_object(
            request,
            Map,
            {'pk': uuid},
            permission='base.view_resourcebase',
            permission_msg=_("You are not allowed to view this map.")
        )

        site = site = Site.objects.get_current()
        config = yaml.load(get_template("dashboards/map_detail/config.yml").render({
            "SITE_NAME": site.name,
            "SITE_DOMAIN": site.domain,
            "latitude": map_obj.center_y,
            "longitude": map_obj.center_x,
            "zoom": map_obj.zoom
        }))
        config['slug'] = uuid
        config['title'] = uuid
        config['baselayers'] = build_baselayers()
        config['featurelayers'] = build_featurelayers(request=request, map_obj=map_obj)
        config['servers'] = build_servers()
        return _build_response(request, config, extension)

    elif type == "layer":

        layer = resolve_object(
            request,
            Layer,
            {'typename': uuid, 'service': None},
            permission='base.view_resourcebase',
            permission_msg=_("You are not permitted to view this layer")
        )

        longitude, latitude = getattr(settings, 'DEFAULT_MAP_CENTER', (0, 0));
        zoom = getattr(settings, 'DEFAULT_MAP_ZOOM', 3)
        site = site = Site.objects.get_current()
        config = yaml.load(get_template("dashboards/layer_detail/config.yml").render({
            "SITE_NAME": site.name,
            "SITE_DOMAIN": site.domain,
            "latitude": latitude,
            "longitude": longitude,
            "zoom": zoom
        }))
        config['slug'] = uuid
        config['title'] = uuid
        config['baselayers'] = build_baselayers()
        config['featurelayers'] = build_featurelayers(request=request, layers=[layer])
        config['servers'] = build_servers()
        return _build_response(request, config, extension)

    else:
        return _build_response(request, {}, extension)

def dashboards_api_state(request, type=None, uuid=None, extension="json"):
    if type == "dashboard":
        return _build_response(request, {}, extension)

    elif type == "map":
        map_obj = resolve_object(
            request,
            Map,
            {'pk': uuid},
            permission='base.view_resourcebase',
            permission_msg=_("You are not allowed to view this map.")
        )

        lon, lat = transform(Proj(init='epsg:3857'), Proj(init='epsg:4326'), map_obj.center_x, map_obj.center_y)
        state = {
            "lat": lat,
            "lon": lon,
            "zoom": map_obj.zoom
        }
        return _build_response(request, state, extension)

    elif type == "layer":
        layer = resolve_object(
            request,
            Layer,
            {'typename': uuid, 'service': None},
            permission='base.view_resourcebase',
            permission_msg=_("You are not permitted to view this layer")
        )
        extent = map(float, [layer.bbox_x0, layer.bbox_y0, layer.bbox_x1, layer.bbox_y1])
        state = {
            "view": {
                "extent": extent
            }
        }
        return _build_response(request, state, extension)

    else:
        return _build_response(request, {}, extension)


def dashboards_api_security(request, type=None, uuid=None, extension="json"):
    if type == "dashboard":
        map_obj = get_object_or_404(Dashboard, uuid=uuid)
        check_perms_view(request, map_obj, raiseErrors=True)
        return _build_response(request, expand_perms(map_obj), extension)

    elif type == "map":

        map_obj = resolve_object(
            request,
            Map,
            {'pk': uuid},
            permission='base.view_resourcebase',
            permission_msg=_("You are not allowed to view this map.")
        )

        allperms_layer = get_users_with_perms(map_obj, attach_perms=True)
        allperms_resourcebase = get_users_with_perms(map_obj.get_self_resource(), attach_perms=True)
        perms = {
            "advertised": True,
            "published": True,
            'view_dashboard': sorted([x.username for x in allperms_resourcebase if 'view_resourcebase' in allperms_resourcebase[x]]),
            'change_dashboard': [],
            'delete_dashboard': []
        }

        return _build_response(request, perms, extension)

    elif type == "layer":

        layer = resolve_object(
            request,
            Layer,
            {'typename': uuid, 'service': None},
            permission='base.view_resourcebase',
            permission_msg=_("You are not permitted to view this layer")
        )

        allperms_layer = get_users_with_perms(layer, attach_perms=True)
        allperms_resourcebase = get_users_with_perms(layer.get_self_resource(), attach_perms=True)
        perms = {
            "advertised": layer.is_published,
            "published": layer.is_published,
            'view_dashboard': sorted([x.username for x in allperms_resourcebase if 'view_resourcebase' in allperms_resourcebase[x]]),
            'change_dashboard': [],
            'delete_dashboard': []
        }

        return _build_response(request, perms, extension)

    else:
        return _build_response(request, {}, extension)


def dashboards_api_schema(request, name=None, extension="json"):
    data = None

    if name == "config":
        data = yaml.load(file(SCHEMA_PATH,'r'))
    elif name == "state":
        data = {}
    elif name == "editor":
        data = yaml.load(get_template("dashboards/editor/schema.yml").render({}))
    elif name == "security":
        data = yaml.load(get_template("dashboards/security/schema.yml").render({}))
    else:
        data = {}

    return _build_response(request, data, extension)

def dashboards_api_endpoints(request, extension="json"):
    return _build_response(request, ENDPOINTS, extension)


def dashboards_api_pages(request, extension="json"):
    return _build_response(request, PAGES, extension)


def dashboards_api_new(request):

    if not request.user.is_authenticated():
        raise Http404("Not authenticated.")

    if request.is_ajax():
        raise Http404("Use AJAX.")

    if request.method != 'POST':
        raise Http404("Can only use POST")

    content = json.loads(request.body)
    config = content['config']
    slug = config.pop('slug', None)

    map_obj = None
    try:
        map_obj = Dashboard.objects.get(slug=slug)
    except Dashboard.DoesNotExist:
        map_obj = None

    response_json = None

    if map_obj:
        response_json = {
            'success': False,
            'message': 'Create new dashboard failed.  Same slug.'
        }
    else:
        title = config.pop('title', None)
        security = content['security']
        map_obj = Dashboard(
          slug=slug,
          title=title,
          config=yaml.dump(config),
          advertised=(security.get('advertised', False) in ["true", "t", "1", "yes", "y", True]),
          published=(security.get('published', False) in ["true", "t", "1", "yes", "y", True]))
        map_obj.save()

        geodash_assign_default_perms(map_obj, request.user)

        config.update({
            'slug': slug,
            'title': title
        })
        response_json = {
            'success': True,
            'config': config
        }

    return HttpResponse(json.dumps(response_json), content_type="application/json")


def dashboards_api_save(request, slug=None):

    if not request.user.is_authenticated():
        raise Http404("Not authenticated.")

    if request.is_ajax():
        raise Http404("Use AJAX.")

    if request.method != 'POST':
        raise Http404("Can only use POST")

    map_obj = get_object_or_404(Dashboard, slug=slug)

    response_json = None

    if request.user.has_perm("change_dashboard", map_obj):

        print request.body
        content = json.loads(request.body)
        config = content['config']
        map_obj.slug = config.pop('slug', None)
        map_obj.title = config.pop('title', None)
        map_obj.config = yaml.dump(config)
        security = content['security'];
        map_obj.advertised=(security.get('advertised', False) in ["true", "t", "1", "yes", "y", True]);
        map_obj.published=(security.get('published', False) in ["true", "t", "1", "yes", "y", True]);
        map_obj.save()

        perms = {
            'view_dashboard': security.get("view_dashboard", []),
            'change_dashboard': security.get("change_dashboard", []),
            'delete_dashboard': security.get("delete_dashboard", [])
        }
        currentUsers = get_users_with_perms(map_obj)
        for perm in ["view_dashboard", "change_dashboard", "delete_dashboard"]:
            # Remove Old Permissions
            for user in currentUsers:
                username = user.username
                if (username not in perms[perm]) and user.has_perm(perm, map_obj):
                    remove_perm(perm, user, map_obj)

            # Add New Permissions
            for username in perms[perm]:
                user = Profile.objects.get(username=username)
                assign_perm(perm, user, map_obj)
                #UserObjectPermission.objects.assign_perm(
                #    perm,
                #    user=user,
                #    obj=map_obj)

        config.update({
            'slug': map_obj.slug,
            'title': map_obj.title
        })
        response_json = {
            'success': True,
            'config': config
        }
    else:
        response_json = {
            'success': False,
            'message': 'Save dashboard failed.  You do not have permissions.'
        }
    return HttpResponse(json.dumps(response_json), content_type="application/json")
