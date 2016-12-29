# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from tastypie.api import Api

from django.conf import settings

from .api import TagResource, TopicCategoryResource, ProfileResource, \
    GroupResource, RegionResource, OwnersResource
from .resourcebase_api import LayerResource, MapResource, DocumentResource, \
    ResourceBaseResource, FeaturedResourceBaseResource

if getattr(settings, "GEODASH_ENABLED", False) and "geonode.contrib.dashboards" in settings.INSTALLED_APPS:
    from .resourcebase_api import DashboardResource

api = Api(api_name='api')

api.register(LayerResource())
api.register(MapResource())
api.register(DocumentResource())
if getattr(settings, "GEODASH_ENABLED", False) and "geonode.contrib.dashboards" in settings.INSTALLED_APPS:
    api.register(DashboardResource())
api.register(ProfileResource())
api.register(ResourceBaseResource())
api.register(TagResource())
api.register(RegionResource())
api.register(TopicCategoryResource())
api.register(GroupResource())
api.register(FeaturedResourceBaseResource())
api.register(OwnersResource())
