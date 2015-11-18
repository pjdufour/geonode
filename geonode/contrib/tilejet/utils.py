import json, os, datetime

import StringIO
from PIL import Image, ImageEnhance

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from tilejetcache.cache import getTileFromCache, get_from_cache, check_cache_availability
from tilejetlogs.mongodb import clearLogs, reloadLogs
from tilejetstats.mongodb import clearStats, reloadStats
from tilejetutil.base import webmercator_bbox
from tilejetutil.tilemath import flip_y, tms_to_bbox, quadkey_to_tms, tms_to_quadkey, bbox_intersects
from tilejetutil.nav import getNearbyTiles, getChildrenTiles, getParentTiles
from tilejetutil.tilefactory import blankTile, redTile, solidTile

from .enumerations import TYPE_TMS, TYPE_TMS_FLIPPED, TYPE_BING, TILEJET_CACHES


def getRegexValue(match,name):
    value = None
    try:
        value = match.group(name)
    except:
        value = None
    return value


def getIPAddress(request):
    ip = None
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = None
    return ip


def getYValues(tileservice, tilesource, ix, iy, iz):

    iyf = -1
    if tilesource['type'] == TYPE_TMS_FLIPPED or tilesource['type'] == TYPE_BING:
        iyf = iy
        iy = flip_y(ix,iyf,iz,256,webmercator_bbox)
    else:
        iyf = flip_y(ix,iy,iz,256,webmercator_bbox)
    
    return (iy, iyf)


def bbox_intersects_source(tilesource,ix,iyf,iz):
    intersects = False
    if tilesource.get('extents', None):
        tile_bbox = tms_to_bbox(ix,iyf,iz)
        for extent in tilesource['extents'].split(';'):
            if bbox_intersects(tile_bbox,map(float,extent.split(','))):
                intersects = True
                break

    return intersects


def _requestTile(request, tileservice=None, tilesource=None, tileorigin=None, z=None, x=None, y=None, u=None, ext=None):

    print "_requestTile"

    now = datetime.datetime.now()
    ip = getIPAddress(request)

    if not tileorigin:
        tileorigin = tilesource['origin']

    verbose = True
    ix = None
    iy = None
    iyf = None
    iz = None

    if u:
        iz, ix, iy = quadkey_to_tms(u)

    elif x and y and z:
        ix = int(x)
        iy = int(y)
        iz = int(z)

        if tilesource['type'] == TYPE_BING:
            u = tms_to_quadkey(ix, iy, iz)

    iy, iyf = getYValues(tileservice,tilesource,ix,iy,iz)

    tile_bbox = tms_to_bbox(ix,iy,iz)

    #Check if requested tile is within source's extents
    returnBlankTile = False
    returnErrorTile = False
    intersects = True
    if tilesource.get('extents', None):
        intersects = bbox_intersects_source(tilesource,ix,iyf,iz)
        if not intersects:
           returnBlankTile = True

    validZoom = 0
    #Check if inside source zoom levels
    if tilesource['minZoom'] or tilesource['maxZoom']:
        if (tilesource['minZoom'] and iz < tilesource['minZoom']):
            validZoom = -1
        elif (tilesource['maxZoom'] and iz > tilesource['maxZoom']):
           validZoom = 1

        if validZoom != 0:
            returnErrorTile = True 

    if returnBlankTile:
        print "responding with blank image"
        image = blankTile(width=256, height=256)
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        return response

    if returnErrorTile:
        print "responding with a red image"
        image = redTile(width=256, height=256)
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        return response

    tile = None
    if tilesource['cacheable'] and iz >= settings.TILEJET_OPTIONS['cache']['memory']['minZoom'] and iz <= settings.TILEJET_OPTIONS['cache']['memory']['maxZoom']:
        key = ",".join([tilesource['name'],str(iz),str(ix),str(iy),ext])
        tilecache, tile = getTileFromCache(
            TILEJET_CACHES['tiles']['LOCATION'],
            TILEJET_CACHES['tiles'],
            'tiles',
            key,
            True,
            GEVENT_MONKEY_PATCH=settings.TILEJET_GEVENT_MONKEY_PATCH_ENABLED)

        if not tilecache:
            print "Error: Could not connect to cache (tiles)."
            line = "Error: Could not connect to cache (tiles)."
            #logTileRequestError(line, now)

        if tile:
            if verbose:
                print "cache hit for "+key
            #logTileRequest(tileorigin, tilesource['name'], x, y, z, 'hit', now, ip)
        else:
            if tilecache and verbose:
                print "cache miss for "+key
            #logTileRequest(tileorigin, tilesource['name'], x, y, z, 'miss', now, ip)

            if tilesource['type'] == TYPE_TMS:
                tile = requestTileFromSource(tilesource=tilesource,x=ix,y=iy,z=iz,ext=ext)
            elif tilesource['type'] == TYPE_TMS_FLIPPED:
                tile = requestTileFromSource(tilesource=tilesource,x=ix,y=iyf,z=iz,ext=ext)
            elif tilesource['type'] == TYPE_BING:
                tile = requestTileFromSource(tilesource=tilesource,u=u,ext=ext)

            try:
                tilecache.set(key, tile)
            except:
                print "Error: Could not write back tile synchronously."

    else:
        if verbose:
            print "cache bypass for "+tilesource['name']+"/"+str(iz)+"/"+str(ix)+"/"+str(iy)
        #logTileRequest(tileorigin, tilesource['name'], x, y, z, 'bypass', now, ip)

        if tilesource['type'] == TYPE_TMS:
            tile = requestTileFromSource(tilesource=tilesource,x=ix,y=iy,z=iz,ext=ext)
        elif tilesource['type'] == TYPE_TMS_FLIPPED:
            tile = requestTileFromSource(tilesource=tilesource,x=ix,y=iyf,z=iz,ext=ext)
        elif tilesource['type'] == TYPE_BING:
            tile = requestTileFromSource(tilesource=tilesource,u=u,ext=ext)

    if not tile:
        print "responding with a red image"
        image = redTile(width=256, height=256)
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        return response

    image = Image.open(StringIO.StringIO(tile['data']))
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response


def make_request(url, params, auth=None, data=None, contentType=None, GEVENT_MONKEY_PATCH=False):
    """
    Prepares a request from a url, params, and optionally authentication.
    """
    if GEVENT_MONKEY_PATCH:
        try:
            from gevent import monkey
            monkey.patch_all()
        except:
            print "gevent monkey patch failed"

    import urllib
    import urllib2

    if params:
        url = url + '?' + urllib.urlencode(params)

    req = urllib2.Request(url, data=data)

    if auth:
        req.add_header('AUTHORIZATION', 'Basic ' + auth)

    if contentType:
        req.add_header('Content-type', contentType)
    else:
        if data:
            req.add_header('Content-type', 'text/xml')


    return urllib2.urlopen(req)


def requestTileFromSource(tilesource=None, x=None, y=None, z=None, u=None, ext=None):
    print "requestTileFromSource"

    if tilesource['type'] == TYPE_BING:
        if tilesource['auth']:
            url = tilesource['url'].format(u=u,ext=ext,auth=ts['auth'])
        else:
            url = tilesource['url'].format(u=u,ext=ext)
    else:
        if tilesource.get('auth', None):
            url = tilesource['url'].format(x=x,y=y,z=z,ext=ext,auth=ts['auth'])
        else:
            url = tilesource['url'].format(x=x,y=y,z=z,ext=ext)

    contentType = "image/png"
    print "URL: "+url
    params = None
    request = make_request(url=url, params=params, auth=None, data=None, contentType=contentType, GEVENT_MONKEY_PATCH=settings.TILEJET_GEVENT_MONKEY_PATCH_ENABLED)
    if request.getcode() != 200:
        raise Exception("Could not fetch tile from source with url {url}: Status Code {status}".format(url=url,status=request.getcode()))
    image = request.read()
    info = request.info()
    headers = {
      'Expires': (info.get('Expires', '') if info else '')
    }
    tile = {
        'headers': headers,
        'data': image
    }
    return tile
