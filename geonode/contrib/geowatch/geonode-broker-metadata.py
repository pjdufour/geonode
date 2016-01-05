# from multiprocessing import Process, Lock, Queue, cpu_count

from geowatchutil.runtime import build_broker_kwargs

from django.conf import settings

from geonode.contrib.geowatch import templates
from geonode.contrib.geowatch.broker.geonode_broker_metadata import GeoNodeBrokerMetadata

verbose = True
broker_config = settings.GEOWATCH_BROKER_METADATA
broker_kwargs = build_broker_kwargs(
    broker_config,
    settings.GEOWATCH_CONFIG,
    templates=templates,
    verbose=verbose)

print "KWARGS: ", broker_kwargs

broker = GeoNodeBrokerMetadata(
    broker_config.get('name', None),
    broker_config.get('description', None),
    **broker_kwargs)
broker.run()
