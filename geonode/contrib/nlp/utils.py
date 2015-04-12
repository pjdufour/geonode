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

from geonode.base.models import Region

sys.path.append(settings.NLP_LIBRARY_PATH)
from mitie import *


def nlp_extract_metadata_core(tile=None, abstract=None, purpose=None):

    if title or abstract or purpose:
        text= ""
        if title:
            text += title + "\n\n"
        if abstract:
            text += abstract + "\n\n"
        if purpose:
            text += purpose + "\n\n"

        ner = named_entity_extractor(settings.NLP_MODEL_PATH)
        tokens = tokenize(text)
        entities = ner.extract_entities(tokens)
        locations = []
        organizations = []
        for e in entities:
            range = e[0]
            tag = e[1]
            score = e[2]
            score_text = "{:0.3f}".format(score)
            entity_text = " ".join(tokens[i] for i in range)
            if tag == "LOCATION":
                locations.append((entity_text, score))
            elif tag == "ORGANIZATION":
                organizations.append((entity_text, score))

        regions = []
        for location in locations:
            location_text, score = location
            if score > settings.NLP_LOCATION_THRESHOLD:
                region = Region.objects.get(name=location_text)
                if region:
                    regions.append(region)

        keywords = []

        return (regions, keywords)

    else:
        return None
