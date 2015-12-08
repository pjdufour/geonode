import json
import time
import unittest

#from geowatchutil.store.geowatch_store_wfs import GeoWatchStoreWFS
from geowatchutil.runtime import provision_broker
from geowatchutil.simulate import simulate_messages_geojson
from geowatchutil.broker.enumerations import GEOWATCH_BROKER_BUILTIN_1, GEOWATCH_BROKER_BUILTIN_2, GEOWATCH_BROKER_BUILTIN_3

from django.conf import settings


class TestBrokers(unittest.TestCase):
    """
    Used to test the GeoWatchStoreWFS stores
    """

    def test_1(self):
        """
        --(GeoJSON)--> Kinesis
        """
        skip = True
        if skip:
            return
        verbose = False
        print "========================"
        print "test_1"
        broker = provision_broker(GEOWATCH_BROKER_BUILTIN_1, globalconfig=settings.GEOWATCH_CONFIG, verbose=verbose)
        messages = simulate_messages_geojson(settings.GEOWATCH_TEST_LAYER)
        broker.receive_messages(messages=messages)
        #broker.delete_topics()  # delete any topics/streams created.
        broker.close()

    def test_2(self):
        """
        --(GeoJSON)--> Kinesis --(GeoJSON)
        """
        skip = True
        if skip:
            return
        verbose = False
        print "========================"
        print "test_2"
        # Producer
        broker1 = provision_broker(GEOWATCH_BROKER_BUILTIN_1, globalconfig=settings.GEOWATCH_CONFIG, verbose=verbose)
        # Need to initialize Broker 2 first, because default shard_it_type is LATEST.
        broker2 = provision_broker(GEOWATCH_BROKER_BUILTIN_2, globalconfig=settings.GEOWATCH_CONFIG, verbose=verbose)
        messages1 = simulate_messages_geojson(settings.GEOWATCH_TEST_LAYER)
        broker1.receive_messages(messages=messages1)  # send to Kinesis
        print "Sleeping for 3 seconds to wait for messages to propogate"
        time.sleep(3)
        messages2 = broker2._cycle_in()  # Retrieve from Kinesis
        # Clean up
        #broker1.delete_topics()  # delete any topics/streams created.
        broker1.close()
        #broker2.delete_topics()  # delete any topics/streams created.
        broker2.close()
        if verbose:
            print "Messages 1:", messages1
            print "----------------------"
            print "Messages 2:", messages2
        self.assertEqual(json.dumps(messages1), json.dumps(messages2))

    def test_3(self):
        """
        --(GeoJSON)--> Kinesis --(GeoJSON)--> WFS
        """
        skip = True
        if skip:
            return
        verbose = False
        print "========================"
        print "test_3"
        # Producer
        broker1 = provision_broker(GEOWATCH_BROKER_BUILTIN_1, globalconfig=settings.GEOWATCH_CONFIG, verbose=verbose)
        # Need to initialize Broker 2 first, because default shard_it_type is LATEST.
        broker2 = provision_broker(GEOWATCH_BROKER_BUILTIN_3, globalconfig=settings.GEOWATCH_CONFIG, verbose=verbose)
        messages1 = simulate_messages_geojson(settings.GEOWATCH_TEST_LAYER)
        broker1.receive_messages(messages=messages1)  # send to Kinesis
        print "Sleeping for 3 seconds to wait for messages to propogate"
        time.sleep(3)
        messages2 = broker2._cycle_in()  # Retrieve from Kinesis
        # Clean up
        #broker1.delete_topics()  # delete any topics/streams created.
        broker1.close()
        #broker2.delete_topics()  # delete any topics/streams created.
        broker2.close()
        if verbose:
            print "Messages 1:", messages1
            print "----------------------"
            print "Messages 2:", messages2
        self.assertEqual(json.dumps(messages1), json.dumps(messages2))

    def test_slack(self):
        """
        --(JSON)--> Slack Notification
        """
        verbose = True
        from geonode.layers.models import Layer
        from geonode.contrib.geowatch.factory import build_geowatch_message_resource
        print "========================"
        print "test_slack"
        if not settings.GEOWATCH_BROKER_TEST_SLACK:
            return
        broker = provision_broker(settings.GEOWATCH_BROKER_TEST_SLACK, globalconfig=settings.GEOWATCH_CONFIG, verbose=verbose)
        messages = []
        for resource in Layer.objects.all()[:2]:
            for actiontype in ['new', 'edit', 'delete']:
                messages.append(build_geowatch_message_resource(actiontype, resource))
        if verbose:
            print "Messages:", messages
        broker.receive_messages(messages=messages)
        #broker.delete_topics()  # delete any topics/streams created.
        broker.close()
