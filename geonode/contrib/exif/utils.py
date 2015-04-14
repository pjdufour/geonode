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

import os
import sys
import httplib2
import base64
import math
import copy
import string
import datetime
import re
from osgeo import ogr
from slugify import Slugify

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.http import HttpResponse
from django.core.cache import cache
from django.http import Http404

from taggit.models import Tag

from geonode.base.models import Region

from slugify import Slugify

import iso8601

from datetime import datetime

custom_slugify = Slugify(separator='_')

def convertExifDateToDjangoDate(date):
   a = list(date.replace(" ","T"))
   a[4] = "-"
   a[7] = "-"
   a[10] = "T"
   #date = iso8601.parse_date("".join(a) + "Z")
   #return date.strftime('%Y-%m-%d %H:%M')

   return datetime(
       int("".join(a[0:4])),
       int("".join(a[5:7])),
       int("".join(a[8:10])),
       int("".join(a[11:13])),
       int("".join(a[14:16]))
   )

def exif_extract_metadata_doc(doc):

    if not doc: 
        return (None, None)

    if not doc.doc_file:
        return (None, None)

    if os.path.splitext(doc.doc_file.name)[1].lower()[1:] in ["jpg","jpeg"]:
        from PIL import Image, ExifTags
        img = Image.open(doc.doc_file.path)
        #exif_data = img._getexif()
        exif_data = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
                if k in ExifTags.TAGS
        }
        print exif_data

        date = None
        regions = []
        keywords = []

        # Extract Date from Exif Data
        if "DateTime" in exif_data:
            date = exif_data["DateTime"]
        if "DateTimeOriginal" in exif_data:
            date = exif_data["DateTimeOriginal"]
        elif "DateTimeDigitized" in exif_data:
            date = exif_data["DateTimeDigitized"]

        if date:
            date = convertExifDateToDjangoDate(date)

        if "Make" in exif_data:
            keywords.append(custom_slugify(exif_data["Make"]))
        if "Model" in exif_data:
            keywords.append(custom_slugify(exif_data["Model"]))

        if "GPSInfo" in exif_data:
            gpsinfo = {}
            for key in exif_data["GPSInfo"].keys():
                decode = ExifTags.GPSTAGS.get(key,key)
                gpsinfo[decode] = exif_data["GPSInfo"][key]
            print gpsinfo

        return (date, None, keywords)
    else:
        return (None, None)
