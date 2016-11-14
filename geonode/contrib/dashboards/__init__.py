#-----------------------------
# Caching
GEODASH_DB_CONN_STR = "dbname='geodash' user='geodash' host='localhost' password='geodash'"
GEODASH_CACHE_DATA = True
GEODASH_MEMCACHED_HOST = 'localhost'
GEODASH_MEMCACHED_PORT = 11212  # So doesn't interfer with root/built-in memcached
#-----------------------------
# DNS Prefetch
GEODASH_DNS_PREFETCH = [
    '//wfp.org',
    '//mapbox.com', '//api.mapbox.com',
    '//thunderforest.com',
    '//openstreetmap.org', '//openstreetmap.fr'
]
#-----------------------------
# Static Management
GEODASH_STATIC_MONOLITH_CSS = False
GEODASH_STATIC_MONOLITH_JS = True
GEODASH_STATIC_VERSION="0.0.1"
#-----------------------------
# Dependencies Management
GEODASH_STATIC_DEPS = {
    "angular": {
        "version": "1.4.0-beta.4"
    },
    "bootstrap": {
        "version": "3.3.5"
    },
    "c3": {
        "version": "0.4.10"
    },
    "d3": {
        "version": "3.5.14"
    },
    "fontawesome": {
        "version": "4.5.0"
    },
    "jquery": {
        "version": "1.9.1"
    },
    "jqueryui": {
        "version": "1.11.4",
        "theme": "cupertino"
    },
    "leaflet": {
        "version": "1.0.0-b1"
    },
    "select2": {
        "version": "4.0.1"
    }
}
#-----------------------------
# Debugging & Testing
GEODASH_STATIC_DEBUG = {
    "main": True,
    "polyfill": False,
    "angular": True,
    "c3": False,
    "d3": False,
    "bootstrap": False,
    "jquery": False,
    "leaflet": True,
    "select2": True,
    'monolith': True
}
