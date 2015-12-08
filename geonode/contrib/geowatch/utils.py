from geowatchutil.runtime import provision_brokers

from django.conf import settings

from geonode.contrib.geowatch import templates
from geonode.contrib.geowatch.mappings import forward_layer, forward_map, forward_document, forward_group, forward_user

from geonode.groups.models import GroupProfile
from geonode.people.models import Profile


def geowatch_run(actiontype, instance):
    m = None
    targettype = None
    if isinstance(instance, GroupProfile):
        m = build_geowatch_message_group(actiontype, instance)
        targettype = 'group'
    elif isinstance(instance, Profile):
        m = build_geowatch_message_user(actiontype, instance)
        targettype = 'user'
    else:
        m = build_geowatch_message_resource(actiontype, instance)
        targettype = str(instance.polymorphic_ctype)
    brokerfilter = {'actiontype': actiontype, 'targettype': targettype}
    brokers = provision_brokers(
        settings.GEOWATCH_BROKERS_EVENT,
        globalconfig=settings.GEOWATCH_CONFIG,
        templates=templates, 
        brokerfilter=brokerfilter)
    for b in brokers:
        b.receive_message(m)
        b.close()


def geowatch_run_postdelete(message, targettype):
    from geowatchutil.runtime import provision_brokers
    from geonode.contrib.geowatch import templates
    brokers = provision_brokers(
        settings.GEOWATCH_BROKERS_EVENT,
        globalconfig=settings.GEOWATCH_CONFIG,
        templates=templates,
        brokerfilter={'actiontype': 'delete', 'targettype': targettype})
    for b in brokers:
        b.receive_message(message)
        b.close()

def build_geowatch_message_resource(actiontype, resource):

    message = {
        'metadata': {
            'actiontype': actiontype,
            'targettype': str(resource.polymorphic_ctype or resource.get_self_resource().polymorphic_ctype)
        }
    }
    data = None
    if str(resource.polymorphic_ctype) == "layer":
        data = forward_layer(resource)
    elif str(resource.polymorphic_ctype) == "map":
        data = forward_map(resource)
    elif str(resource.polymorphic_ctype) == "document":
        data = forward_document(resource)
    message['data'] = data
    return message


def build_geowatch_message_group(actiontype, instance):
    message = {
        'metadata': {
            'actiontype': actiontype,
            'targettype': 'group'
        },
        'data': forward_group(instance)
    }
    return message


def build_geowatch_message_user(actiontype, instance):
    message = {
        'metadata': {
            'actiontype': actiontype,
            'targettype': 'user'
        },
        'data': forward_user(instance)
    }
    return message
