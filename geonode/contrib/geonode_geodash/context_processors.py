try:
    import simplejson as json
except ImportError:
    import json

from django.conf import settings

from geonode.contrib.geonode_geodash.models import GeoDashDashboard

def geonode_geodash(request):
    """Global values to pass to templates"""

    ctx = {
        "GEODASH_DASHBOARDS_TYPEAHEAD": json.dumps([{'id': d.slug, 'text': d.title} for d in GeoDashDashboard.objects.filter(advertised=True, published=True).order_by('title')])  # noqa
    }

    return ctx
