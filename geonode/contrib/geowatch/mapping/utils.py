from geonode.contrib.geowatch.mapping.geowatch_mapping_layer import GeoWatchMappingLayer
from geonode.contrib.geowatch.mapping.geowatch_mapping_map import GeoWatchMappingMap
from geonode.contrib.geowatch.mapping.geowatch_mapping_document import GeoWatchMappingDocument
from geonode.contrib.geowatch.mapping.geowatch_mapping_user import GeoWatchMappingUser
from geonode.contrib.geowatch.mapping.geowatch_mapping_group import GeoWatchMappingGroup


def forward_layer(layer):
    mapping = GeoWatchMappingLayer()
    return mapping.forward(resource=layer)


def forward_map(map_obj):
    mapping = GeoWatchMappingMap()
    return mapping.forward(resource=map_obj)


def forward_document(document):
    mapping = GeoWatchMappingDocument()
    return mapping.forward(resource=document)


def forward_group(group):
    mapping = GeoWatchMappingGroup()
    return mapping.forward(group=group)


def forward_user(user):
    mapping = GeoWatchMappingUser()
    return mapping.forward(user=user)

