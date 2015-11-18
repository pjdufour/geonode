TILEJET_STATS = [
    {'name': 'total', 'collection': 'stats_total', 'attributes': []},
    {'name': 'by_origin', 'collection': 'stats_by_origin', 'attributes': ['origin']},
    {'name': 'by_source', 'collection': 'stats_by_source', 'attributes': ['source']},
    {'name': 'by_zoom', 'collection': 'stats_by_zoom', 'attributes': ['z']},
    {'name': 'by_status', 'collection': 'stats_by_status', 'attributes': ['status']},
    {'name': 'by_year', 'collection': 'stats_by_year', 'attributes': ['year']},
    {'name': 'by_month', 'collection': 'stats_by_month', 'attributes': ['month']},
    {'name': 'by_date', 'collection': 'stats_by_date', 'attributes': ['date']},

    {'name': 'by_year_origin', 'collection': 'stats_by_year_origin', 'attributes': ['year', 'origin']},
    {'name': 'by_year_source', 'collection': 'stats_by_year_source', 'attributes': ['year', 'source']},
    {'name': 'by_date_origin', 'collection': 'stats_by_date_origin', 'attributes': ['date', 'origin']},
    {'name': 'by_date_source', 'collection': 'stats_by_date_source', 'attributes': ['date', 'source']},
    {'name': 'by_origin_status', 'collection': 'stats_by_origin_status', 'attributes': ['origin', 'status']},
    {'name': 'by_source_status', 'collection': 'stats_by_source_status', 'attributes': ['source', 'status']},
    {'name': 'by_month_origin', 'collection': 'stats_by_month_origin', 'attributes': ['month', 'origin']},
    {'name': 'by_month_source', 'collection': 'stats_by_month_source', 'attributes': ['month', 'source']},
    {'name': 'by_zoom_status', 'collection': 'stats_by_zoom_status', 'attributes': ['z', 'status']}
]

TYPE_TMS = 1
TYPE_TMS_FLIPPED = 2
TYPE_BING = 3
TYPE_WMS = 4

TILEJET_ALLOWED_HOSTS = ("*.openstreetmap.org", "*.openstreetmap.fr",)

TILEJET_ORIGINS = {
    "osm_main": {
        "name":"osm_main",
        "description":"Main OpenStreetMap Server",
        "type": TYPE_TMS_FLIPPED,
        "multiple": False,
        "cacheable": True,
        "url": "http://a.tile.openstreetmap.org/{z}/{x}/{y}.{ext}"
    },
    "osm_france": {
        "name": "osm_france",
        "description":"OSM France Server.  This server primarily serves out the humanitarian style OSM tiles.",
        "type": TYPE_TMS_FLIPPED,
        "multiple": True,
        "cacheable": False,
        "url": "http://a.tile.openstreetmap.fr/{slug}/{z}/{x}/{y}.{ext}"
    }
}

TILEJET_SOURCES = {
    "osm": {
        "name": "osm",
        "type": TYPE_TMS_FLIPPED,
        "auto": False,
        "cacheable": True,
        "proxy": True,
        "origin": "osm_main",
        "pattern": "^http://a.tile.openstreetmap.org/(?P<z>[^/]+)/(?P<x>[^/]+)/(?P<y>[^/]+)\\.(?P<ext>(png|gif|jpg|jpeg))$",
        "url": "http://a.tile.openstreetmap.org/{z}/{x}/{y}.{ext}",
        "minZoom": 0,
        "maxZoom": 20
    },
    "osm_humanitarian": {
        "name": "osm_humanitarian",
        "type": TYPE_TMS_FLIPPED,
        "auto": False,
        "cacheable": True,
        "proxy": True,
        "origin": "osm_france",
        "pattern": "^http://a.tile.openstreetmap.fr/hot/(?P<z>[^/]+)/(?P<x>[^/]+)/(?P<y>[^/]+)\\.(?P<ext>(png|gif|jpg|jpeg))$",
        "url": "http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.{ext}",
        "minZoom": 0,
        "maxZoom": 20

    }
}

TILEJET_CACHES = {
    'default': {
        'BACKEND': 'memcachepool.cache.UMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'OPTIONS': {
            'MAX_POOL_SIZE': 40,
            'BLACKLIST_TIME': 60,
            'SOCKET_TIMEOUT': 60,
            'MAX_ITEM_SIZE': 1000*1000*1000
        }
    },
    'tiles': {
        'BACKEND': 'memcachepool.cache.UMemcacheCache',
        'LOCATION': '127.0.0.1:11212',
        'OPTIONS': {
            'MAX_POOL_SIZE': 40,
            'BLACKLIST_TIME': 60,
            'SOCKET_TIMEOUT': 5,
            'MAX_ITEM_SIZE': 1000*1000*1000
        }
    }
}
