# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
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

HTML_MESSAGE_TEMPLATES = [
  {
        "actiontype": ["new"],
        "targettype":  ["layer", "map", "document"],
        "template": "A new {type} <a href=\"{url_detail}\">{title}</a> has been added to {sitename} by {owner_name}.  {url_detail}"
  },
  {
        "actiontype": ["edit"],
        "targettype":  ["layer", "map", "document"],
        "template": "A {type} <a href=\"{url_detail}\">{title}</a> has been modified on {sitename} by {owner_name}.  {url_detail}"
  },
  {
        "actiontype": ["delete"],
        "targettype":  ["layer", "map", "document"],
        "template": "The {type} {title} has been deleted from {sitename}.  {baseurl}"
  },
  {
        "actiontype": ["new"],
        "targettype":  ["group"],
        "template": "A new {type} <a href=\"{url_detail}\">{title}</a> has been added to {sitename}.  {url_detail}"
  },
  {
        "actiontype": ["edit"],
        "targettype":  ["group"],
        "template": "A {type} <a href=\"{url_detail}\">{title}</a> has been modified on {sitename}.  {url_detail}"
  },
  {
        "actiontype": ["delete"],
        "targettype":  ["group"],
        "template": "The {type} {title} has been deleted from {sitename}.  {baseurl}"
  },
  {
        "actiontype": ["login"],
        "targettype":  ["user"],
        "template": "User <a href=\"{url_detail}\">{username}</a> has been modified on {sitename}.  {url_detail}"
  }
]

SNS_MESSAGE_TEMPLATES = [
  {
        "actiontype": ["new"],
        "targettype":  ["layer", "map", "document"],
        "template": "A new {type} {title} has been added to {sitename} by {owner_name}.  {url_detail}"
  },
  {
        "actiontype": ["edit"],
        "targettype":  ["layer", "map", "document"],
        "template": "A {type} {title} has been modified on {sitename} by {owner_name}.  {url_detail}"
  },
  {
        "actiontype": ["delete"],
        "targettype":  ["layer", "map", "document"],
        "template": "The {type} {title} has been deleted from {sitename}.  {baseurl}"
  },
  {
        "actiontype": ["new"],
        "targettype":  ["group"],
        "template": "A new {type} {title} has been added to {sitename}.  {url_detail}"
  },
  {
        "actiontype": ["edit"],
        "targettype":  ["group"],
        "template": "A {type} {title} has been modified on {sitename}.  {url_detail}"
  },
  {
        "actiontype": ["delete"],
        "targettype":  ["group"],
        "template": "The {type} {title} has been deleted from {sitename}.  {baseurl}"
  },
  {
        "actiontype": ["login"],
        "targettype":  ["user"],
        "template": "User {username} has been modified on {sitename}.  {url_detail}"
  }
]

SLACK_MESSAGE_TEMPLATES = [
    {
        "actiontype": ["new"],
        "targettype":  ["layer"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "title_link": "{url_detail}",
                "fallback": "A new {type} {title} has been added to {sitename} by {owner_name}.  {url_detail}",
                "text": "A new {type} <{url_detail}|{title}> has been added to "
                        "<{baseurl}|{sitename}> by <{owner_url}|{owner_name}>.",
                "thumb_url": "{thumbnail_url}",
                "fields": [{
                     "title": "Zipped Shapefile",
                     "value": "<{url_shp}|Download>",
                     "short": True
                 },
                 {
                     "title": "GeoJSON",
                     "value": "<{url_geojson}|Download>",
                     "short": True
                 },
                 {
                     "title": "View in Google Earth",
                     "value": "<{url_netkml}|Download>",
                     "short": True
                 },
                 {
                    "title": "View on Map",
                    "value": "<{url_map}|View>",
                    "short": True
                 }],
                 "color": "#000099"
            }]
        }
    },
    {
        "actiontype": ["edit"],
        "targettype":  ["layer"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "title_link": "{url_detail}",
                "fallback": "The {type} {title} has been modified on {sitename} by {owner_name}.  {url_detail}",
                "text": "The {type} <{url_detail}|{title}> has been modified on "
                        "<{baseurl}|{sitename}> by <{owner_url}|{owner_name}>.",
                "thumb_url": "{thumbnail_url}",
                "fields": [{
                     "title": "Zipped Shapefile",
                     "value": "<{url_shp}|Download>",
                     "short": True
                 },
                 {
                     "title": "GeoJSON",
                     "value": "<{url_geojson}|Download>",
                     "short": True
                 },
                 {
                     "title": "View in Google Earth",
                     "value": "<{url_netkml}|Download>",
                     "short": True
                 },
                 {
                     "title": "View on Map",
                     "value": "<{url_map}|View>",
                     "short": True
                 }],
                "color": "#000099"
            }]
        }
    },
    {
        "actiontype": ["delete"],
        "targettype":  ["layer"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "fallback": "The {type} {title} has been deleted from {sitename}.  {baseurl}",
                "text": "The {type} {title} has been deleted from <{baseurl}|{sitename}>.",
                "color": "#FF0000"
            }]
        }
    },
    {
        "actiontype": ["new"],
        "targettype":  ["layer"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "title_link": "{url_detail}",
                "fallback": "A new {type} {title} has been added to {sitename} by {owner_name}.  {url_detail}",
                "text": "A new {type} <{url_detail}|{title}> has been added to "
                        "<{baseurl}|{sitename}> by <{owner_url}|{owner_name}>.",
                "thumb_url": "{thumbnail_url}",
                "fields": [{
                     "title": "View Map",
                     "value": "<{url_view}|View>",
                     "short": True
                 },
                 {
                     "title": "Download Map",
                     "value": "<{url_download}|Download>",
                     "short": True
                 }],
                "color": "#000099"
            }]
        }
    },
    {
        "actiontype": ["edit"],
        "targettype":  ["map"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "title_link": "{url_detail}",
                "fallback": "The {type} {title} has been modified on {sitename} by {owner_name}.  {url_detail}",
                "text": "The {type} <{url_detail}|{title}> has been modified on "
                        "<{baseurl}|{sitename}> by <{owner_url}|{owner_name}>.",
                "thumb_url": "{thumbnail_url}",
                "fields": [{
                     "title": "View Map",
                     "value": "<{url_view}|View>",
                     "short": True
                 },
                 {
                     "title": "Download Map",
                     "value": "<{url_download}|Download>",
                     "short": True
                 }],
                "color": "#000099"
            }]
        }
    },
    {
        "actiontype": ["delete"],
        "targettype":  ["map"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "fallback": "The {type} {title} has been deleted from {sitename}.  {baseurl}",
                "text": "The {type} {title} has been deleted from <{baseurl}|{sitename}>.",
                "color": "#FF0000"
            }]
        }
    },
    {
        "actiontype": ["new"],
        "targettype":  ["document"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "title_link": "{url_detail}",
                "fallback": "A new {type} {title} has been added to {sitename} by {owner_name}.  {url_detail}",
                "text": "A new {type} <{url_detail}|{title}> has been added to "
                        "<{baseurl}|{sitename}> by <{owner_url}|{owner_name}>.",
                "thumb_url": "{thumbnail_url}",
                "fields": [{
                     "title": "Download Document",
                     "value": "<{url_download}|Download>",
                     "short": True
                 }],
                "color": "#000099"
            }]
        }
    },
    {
        "actiontype": ["edit"],
        "targettype":  ["document"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "title_link": "{url_detail}",
                "fallback": "The {type} {title} has been modified on {sitename} by {owner_name}.  {url_detail}",
                "text": "The {type} <{url_detail}|{title}> has been modified on "
                        "<{baseurl}|{sitename}> by <{owner_url}|{owner_name}>.",
                "thumb_url": "{thumbnail_url}",
                "fields": [{
                      "title": "Download Document",
                     "value": "<{url_download}|Download>",
                     "short": True
                 }],
                "color": "#000099"
            }]
        }
    },
    {
        "actiontype": ["delete"],
        "targettype":  ["document"],
        "template": {
            "attachments": [{
                "title": "{title}",
                "fallback": "The {type} {title} has been deleted from {sitename}.  {baseurl}",
                "text": "The {type} {title} has been deleted from <{baseurl}|{sitename}>.",
                "color": "#FF0000"
            }]
        }
    },
    {
        "actiontype": ["new"],
        "targettype":  ["group"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "title_link": "{url_detail}",
                "fallback": "A new {type} {title} has been added to {sitename}.  {url_detail}",
                "text": "A new {type} <{url_detail}|{title}> has been added to "
                        "<{baseurl}|{sitename}>.",
                "thumb_url": "{thumbnail_url}",
                "color": "#000099"
            }]
        }
    },
    {
        "actiontype": ["edit"],
        "targettype":  ["group"],
        "template":
        {
            "attachments": [{
                "title": "{title}",
                "title_link": "{url_detail}",
                "fallback": "The {type} {title} has been modified on {sitename}.  {url_detail}",
                "text": "The {type} <{url_detail}|{title}> has been modified on "
                        "<{baseurl}|{sitename}>.",
                "thumb_url": "{thumbnail_url}",
                "color": "#000099"
            }]
        }
    },
    {
        "actiontype": ["delete"],
        "targettype":  ["group"],
        "template": {
            "attachments": [{
                "title": "{title}",
                "fallback": "The {type} {title} has been deleted from {sitename}.  {baseurl}",
                "text": "The {type} {title} has been deleted from <{baseurl}|{sitename}>.",
                "color": "#FF0000"
            }]
        }
    },
    {
        "actiontype": ["login"],
        "targettype":  ["user"],
        "template":
        {
            "attachments": [{
                "title": "{username}",
                "title_link": "{url_detail}",
                "fallback": "User {username} (with access level {access}) has logged into {sitename}.  {url_detail}",
                "text": "User <{url_detail}|{username}> (with {access} access level) has logged into "
                        "<{baseurl}|{sitename}>.",
                "thumb_url": "{thumbnail_url}",
                "color": "{color}"
            }]
        }
    }
]
