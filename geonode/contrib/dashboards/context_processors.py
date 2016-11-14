try:
    import simplejson as json
except ImportError:
    import json

from django.conf import settings

from geonode.contrib.dashboards.models import Dashboard

def dashboards(request):
    """Global values to pass to templates"""

    GEODASH_DASHBOARDS_TYPEAHEAD = [{'id': d.slug, 'text': d.title} for d in Dashboard.objects.filter(advertised=True, published=True).order_by('title')]
    ctx = {
        "GEODASH_DASHBOARDS_TYPEAHEAD": json.dumps(GEODASH_DASHBOARDS_TYPEAHEAD)  # noqa
    }

    return ctx
