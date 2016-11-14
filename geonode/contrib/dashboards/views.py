import datetime
import requests
import yaml
import errno
from socket import error as socket_error

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template

#from guardian.models import UserObjectPermission
from guardian.shortcuts import get_users_with_perms, get_perms, remove_perm, assign_perm

try:
    import simplejson as json
except ImportError:
    import json

from geonode.people.models import Profile

from geodash.cache import provision_memcached_client
from geodash.utils import build_state_schema, build_context, build_initial_state, build_editor_config, build_dashboard_config
from geodash.security import check_perms_view, expand_perms, geodash_assign_default_perms
from geodash.views import GeoDashDictWriter

from geonode.contrib.dashboards.models import Dashboard
from geonode.contrib.dashboards.utils import expand_users

SCHEMA_PATH = 'geonode/contrib/dashboards/static/dashboards/build/schema/schema.yml'
ENDPOINTS_PATH = 'geonode/contrib/dashboards/static/dashboards/build/api/endpoints.yml'


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

    page = "browse"
    slug = "browse"
    map_obj = get_object_or_404(Dashboard, slug=slug)

    config = yaml.load(map_obj.config)
    ctx = build_context(
        config,
        build_initial_state(config, page=page, slug=slug),
        build_state_schema())

    dashboard_resources = [{ "url": "/api/endpoints.json" }];

    ctx = {
        "dashboard_url": "/api/dashboard/browse.json",
        "state_url": "/api/state/browse.json",
        "state_schema_ul": "/api/schema/state.json",
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
          "main.tpl.html": get_template("sparc2/home/main.tpl.html").render(ctx)
      })
    })

    return render_to_response(template, RequestContext(request, ctx))


def dashboard_page(request, slug=None, template="dashboards/dashboard.html"):

    map_obj = get_object_or_404(Dashboard, slug=slug)

    check_perms_view(request, map_obj, raiseErrors=True)

    config = build_dashboard_config(map_obj)
    config_schema = yaml.load(file(SCHEMA_PATH,'r'))

    editor_template = "geodash/editor/editor.yml"
    editor_yml = get_template(editor_template).render({})
    editor = yaml.load(editor_yml)

    security = expand_perms(map_obj)
    security_schema = yaml.load(get_template("geodash/security/security.yml").render({}))

    ctx = build_context(
        config,
        build_initial_state(config, page="dashboard", slug=slug),
        build_state_schema())

    ctx.update({
        #"pages_json": json.dumps(pages),
        "map_config_schema": config_schema,
        "map_config_schema_json": json.dumps(config_schema),
        "editor": editor,
        "editor_json": json.dumps(editor),
        "security": security,
        "security_json": json.dumps(security),
        "security_schema": security_schema,
        "security_schema_json": json.dumps(security_schema),
        "include_sidebar_right": request.user.has_perm("change_dashboard", map_obj),
        "perms_json": json.dumps(get_perms(request.user, map_obj)),
        "users": json.dumps(expand_users(request, map_obj))
    })

    dashboard_resources = [
        { "url": "/api/endpoints.json" },
        { "name": "editor_schema", "url": reverse("dashboard_schema", kwargs={name: "editor", extension: "json"})},
        { "name": "security_schema", "url": reverse("dashboard_schema", kwargs={name: "security", extension: "json"})}
    ];

    ctx = {
        "dashboard_url": reverse("dashboard_config", kwargs={slug: slug, extension: extension}),
        "state_url": reverse("dashboard_state", kwargs={slug: slug, extension: extension}),
        "state_schema_url": reverse("dashboard_schema_state"),
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
          "main.tpl.html": get_template("dashboards/main.tpl.html").render(ctx)
      })
    })

    return render_to_response(template, RequestContext(request, ctx))


def dashboard_config(request, slug=None, extension="json"):
    map_obj = get_object_or_404(Dashboard, slug=slug)
    check_perms_view(request, map_obj, raiseErrors=True)
    return _build_response(request, build_dashboard_config(map_obj), extension)

def dashboard_state(request, extension="json"):
    return _build_response(request, {}, extension)

def dashboard_security(request, slug=None, extension="json"):
    map_obj = get_object_or_404(Dashboard, slug=slug)
    check_perms_view(request, map_obj, raiseErrors=True)
    return _build_response(request, expand_perms(map_obj), extension)


def dashboard_schema(request, name=None, extension="json"):
    if name == "config":
        return _build_response(request, yaml.load(file(SCHEMA_PATH,'r')), extension)
    elif name == "state":
        return _build_response(request, {}, extension)
    elif name == "security":
        return yaml.load(get_template("geodash/security/security.yml").render({}))

def dashboard_endpoints(request, extension="json"):
    return _build_response(request, yaml.load(file(ENDPOINTS_PATH,'r')), extension)

def dashboard_new(request):

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


def dashboard_save(request, slug=None):

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
