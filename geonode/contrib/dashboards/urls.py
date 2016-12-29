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

from django.conf.urls import url
from geonode.contrib.dashboards import views


urlpatterns = [

    url(
        r'^/?$',
        views.dashboards_browse,
        name='dashboards_browse'),

    url(
        r'^new/(?P<type>[^/]+)/(?P<uuid>[^/]+)?$',
        views.dashboards_new,
        name='dashboards_new'),

    url(
        r'^(?P<uuid>[^/]+)$',
        views.dashboards_page,
        name='dashboards_page'),

    url(
        r'^api/endpoints[.](?P<extension>[^.]+)$',
        views.dashboards_api_endpoints,
        name='dashboards_api_endpoints'),

    url(
        r'^api/pages[.](?P<extension>[^.]+)$',
        views.dashboards_api_pages,
        name='dashboards_api_pages'),

    url(
        r'^api/schema/(?P<name>[^/]+)[.](?P<extension>[^.]+)$',
        views.dashboards_api_schema,
        name='dashboards_api_schema'),

    url(
        r'^api/(?P<type>[^/]+)/(?P<uuid>[^/]+)/config[.](?P<extension>[^.]+)$',
        views.dashboards_api_config,
        name='dashboards_api_config'),

    url(
        r'^api/(?P<type>[^/]+)/(?P<uuid>[^/]+)/state[.](?P<extension>[^.]+)$',
        views.dashboards_api_state,
        name='dashboards_api_state'),

    url(
        r'^api/(?P<type>[^/]+)/(?P<uuid>[^/]+)/security[.](?P<extension>[^.]+)$',
        views.dashboards_api_security,
        name='dashboards_api_security'),


    url(
        r'^api/(?P<type>[^/]+)/new[.](?P<extension>[^.]+)$',
        views.dashboards_api_new,
        name='dashboards_api_new'),

    url(
        r'^api/(?P<type>[^/]+)/(?P<uuid>[^/]+)/save[.](?P<extension>[^.]+)$',
        views.dashboards_api_save,
        name='dashboards_api_save'),

]
