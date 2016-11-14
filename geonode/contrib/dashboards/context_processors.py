try:
    import simplejson as json
except ImportError:
    import json

from django.conf import settings

from geonode.contrib.dashboards.models import Dashboard
from geodash.enumerations import MONTHS_NUM, MONTHS_LONG, MONTHS_SHORT3, MONTHS_ALL, DAYSOFTHEWEEK

def dashboards(request):
    """Global values to pass to templates"""

    GEODASH_DASHBOARDS_TYPEAHEAD = [{'id': d.slug, 'text': d.title} for d in Dashboard.objects.filter(advertised=True, published=True).order_by('title')]
    ctx = {
        "MONTHS_NUM": MONTHS_NUM,
        "MONTHS_SHORT3": MONTHS_SHORT3,
        "MONTHS_LONG": MONTHS_LONG,
        "MONTHS_ALL": MONTHS_ALL,
        "DAYSOFTHEWEEK": DAYSOFTHEWEEK,
        "GEODASH_STATIC_VERSION": settings.GEODASH_STATIC_VERSION,
        "GEODASH_STATIC_DEBUG": settings.GEODASH_STATIC_DEBUG,
        "GEODASH_STATIC_DEPS": settings.GEODASH_STATIC_DEPS,
        "GEODASH_DNS_PREFETCH": settings.GEODASH_DNS_PREFETCH,
        "GEODASH_STATIC_MONOLITH_CSS": settings.GEODASH_STATIC_MONOLITH_CSS,
        "GEODASH_STATIC_MONOLITH_JS": settings.GEODASH_STATIC_MONOLITH_JS,
        "GEODASH_MAPPING_LIBRARY": settings.GEODASH_MAPPING_LIBRARY,
        "GEODASH_DASHBOARDS_TYPEAHEAD": json.dumps(GEODASH_DASHBOARDS_TYPEAHEAD)  # noqa
    }

    return ctx
