import json, os, datetime

from urlparse import urlsplit

from tilejetutil.tileregex import match_pattern_url

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import validate_host
from django.template import RequestContext
from django.utils.http import is_safe_url

from .enumerations import TILEJET_ALLOWED_HOSTS, TILEJET_SOURCES
from .utils import _requestTile, getRegexValue


def proxy(request):
    host = None

    if 'url' not in request.GET:
        return HttpResponse("The proxy service requires a URL-encoded URL as a parameter.",
                            status=400,
                            content_type="text/plain"
                            )

    raw_url = request.GET['url']
    url = urlsplit(raw_url)
    locator = url.path
    if url.query != "":
        locator += '?' + url.query
    if url.fragment != "":
        locator += '#' + url.fragment

    if not settings.DEBUG:
        if not validate_host(url.hostname, TILEJET_ALLOWED_HOSTS):
            return HttpResponse("DEBUG is set to False but the host of the path provided to the proxy service"
                                " is not in the PROXY_ALLOWED_HOSTS setting.",
                                status=403,
                                content_type="text/plain"
                                )
    #headers = {}

    #if settings.SESSION_COOKIE_NAME in request.COOKIES and is_safe_url(url=raw_url, host=host):
    #    headers["Cookie"] = request.META["HTTP_COOKIE"]

    #if request.method in ("POST", "PUT") and "CONTENT_TYPE" in request.META:
    #    headers["Content-Type"] = request.META["CONTENT_TYPE"]

    print "Raw URL: "+ raw_url
    match_regex = None
    match_tilesource = None

    for key, tilesource in TILEJET_SOURCES.iteritems():
        if tilesource['proxy']:
            print "testing: "+tilesource['pattern']
            match = match_pattern_url(tilesource['pattern'], raw_url)
            if match:
                match_regex = match
                match_tilesource = tilesource
                break

    if match_tilesource and match_regex:
        return proxy_tilesource(request, match_tilesource, match_regex)
    else:
        return HttpResponse(
            content = 'No matching tilesource found.',
            status=404,
            content_type="text/plain")


def proxy_tilesource(request, tilesource, match):
    if tilesource:
        z, x, y, u, ext = None, None, None, None, None
        z = getRegexValue(match, 'z')
        x = getRegexValue(match, 'x')
        y = getRegexValue(match, 'y')
        u = getRegexValue(match, 'u')
        ext = getRegexValue(match, 'ext')

        return _requestTile(
            request,
            tileservice=None,
            tilesource=tilesource,
            z=z,x=x,y=y,u=u,ext=ext)
    else:
        return HttpResponse(RequestContext(request, {}), status=404)


@login_required
def flush(request):
   
    # Using raw umemcache flush_all function

    #defaultcache = umemcache.Client(settings.CACHES['default']['LOCATION'])
    #defaultcache.connect()
    #defaultcache.flush_all()

    #tilecache = umemcache.Client(settings.CACHES['tiles']['LOCATION'])
    #tilecache.connect()
    #tilecache.flush_all()

    #resultscache = umemcache.Client(settings.CACHES['tiles']['LOCATION'])
    #resultscache.connect()
    #resultscache.flush_all()

    #==#

    # Using custom clear function from https://github.com/mozilla/django-memcached-pool/blob/master/memcachepool/cache.py
    if(check_cache_availability(settings.CACHES['default']['LOCATION'], settings.CACHES['default'])):
        defaultcache = caches['default']
        defaultcache.clear()

    if(check_cache_availability(settings.CACHES['tiles']['LOCATION'], settings.CACHES['tiles'])):
        tilecache = caches['tiles']
        tilecache.clear()

    if(check_cache_availability(settings.CACHES['celery_results']['LOCATION'], settings.CACHES['celery_results'])):
        resultscache = caches['celery_results']
        resultscache.clear()

    return HttpResponse("Tile cache flushed.",
                        content_type="text/plain"
                        )


@login_required
def stats_json(request):
    stats = None
    if settings.STATS_SAVE_MEMORY:
        cache, stats = get_from_cache(
            settings.CACHES['default']['LOCATION'],
            settings.CACHES['default'],
            'default',
            'stats_tilerequests',
            GEVENT_MONKEY_PATCH=settings.TILEJET_GEVENT_MONKEY_PATCH)
    if settings.STATS_SAVE_FILE and not stats:
        stats = get_from_file(settings.STATS_REQUEST_FILE, filetype='json')
    if not stats:
        stats = {}
    return HttpResponse(json.dumps(stats),
                        content_type="application/json"
                        )
