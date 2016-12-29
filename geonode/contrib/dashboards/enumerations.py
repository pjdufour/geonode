from django.conf import settings
from django.core.urlresolvers import reverse

ENDPOINTS = {
  "GEONODE_DASHBOARDS" : reverse("api_dispatch_list", kwargs={"api_name": "api", "resource_name": "dashboards"}),
  "GEONODE_PROFILES" : reverse("api_dispatch_list", kwargs={"api_name": "api", "resource_name": "profiles"}),
  "DOWNLOAD_CONFIG_JSON": "/dashboards/api/dashboard/{{ slug }}/config.json",
  "DOWNLOAD_CONFIG_YAML": "/dashboards/api/dashboard/{{ slug }}/config.yml",
  "DOWNLOAD_SECURITY_JSON": "/dashboards/api/dashboard/{{ slug }}/security.json",
  "DOWNLOAD_SECURITY_YAML": "/dashboards/api/dashboard/{{ slug }}/security.yml",
  "DASHBOARD_SAVE_JSON": "/dashboards/api/dashboard/{{ slug }}/save.json"
}

PAGES = {
    "browse": settings.SITEURL[:-1]+"/dashboards/",
    "dashboard": settings.SITEURL[:-1]+"/dashboards/{{ slug }}"
}
