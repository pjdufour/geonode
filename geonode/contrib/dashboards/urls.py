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
        r'^dashboard/(?P<slug>[^/]+)$',
        views.dashboard_page,
        name='dashboard_page'),

    url(
        r'^api/endpoints[.](?P<extension>[^.]+)$',
        views.dashboard_endpoints,
        name='dashboard_endpoints'),

    url(
        r'^api/schema/(?P<name>[^/]+)[.](?P<extension>[^.]+)$',
        views.dashboard_schema,
        name='dashboard_schema'),

    url(
        r'^api/config/(?P<slug>[^/]+)[.](?P<extension>[^.]+)$',
        views.dashboard_config,
        name='dashboard_config'),

    url(
        r'^api/state/(?P<slug>[^/]+)[.](?P<extension>[^.]+)$',
        views.dashboard_state,
        name='dashboard_state'),

    url(
        r'^api/security/(?P<slug>[^/]+)[.](?P<extension>[^.]+)$',
        views.dashboard_security,
        name='dashboard_security'),


    url(
        r'^api/new$',
        views.dashboard_new,
        name='dashboard_new'),

    url(
        r'^api/save/(?P<slug>[^/]+)$',
        views.dashboard_save,
        name='dashboard_save'),

]
