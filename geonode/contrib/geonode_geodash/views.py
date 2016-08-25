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

from guardian.models import UserObjectPermission
from guardian.shortcuts import get_users_with_perms, get_perms, remove_perm

try:
    import simplejson as json
except ImportError:
    import json

from geodash.cache import provision_memcached_client
from geodash.utils import build_state_schema

from geodashserver.geodash.models import GeoDashDashboard
from geodashserver.security import check_perms_view, expand_perms, expand_users, geodash_assign_default_perms
from geodashserver.utils import build_context, build_initial_state, build_editor_config, build_dashboard_config

SCHEMA_PATH = 'geodashserver/static/geodashserver/build/schema/schema.yml'

def geodash_browse(request, template="geonode_geodash/geodash_browse.html"):
    now = datetime.datetime.now()
    current_month = now.month

    page = "browse"
    slug = "browse"
    map_obj = get_object_or_404(GeoDashDashboard, slug=slug)

    config = yaml.load(map_obj.config)
    ctx = build_context(
        config,
        build_initial_state(config, page=page, slug=slug),
        build_state_schema())
    ctx["include_sidebar_right"] = False

    return render_to_response(template, RequestContext(request, ctx))

def geodash_dashboard_config(request, slug=None, extension="json"):

    map_obj = get_object_or_404(GeoDashDashboard, slug=slug)
    check_perms_view(request, map_obj, raiseErrors=True)
    map_config = build_dashboard_config(map_obj)

    ext_lc = extension.lower();
    if ext_lc == "json":
        return HttpResponse(json.dumps(map_config, default=jdefault), content_type="application/json")
    elif ext_lc == "yml" or ext_lc == "yaml":
        response = yaml.safe_dump(map_config, encoding="utf-8", allow_unicode=True, default_flow_style=False)
        return HttpResponse(response, content_type="application/json")
    else:
        raise Http404("Unknown config format.")

def geodash_map_schema(request):
    map_config_schema = yaml.load(file(SCHEMA_PATH,'r'))
    return HttpResponse(json.dumps(map_config_schema, default=jdefault), content_type="application/json")
