# Dashboards Contrib App

Dashboards is a contrib app for quickly producing visualizations of geospatial data.  It is built on GeoDash.

### GeoDash

The name comes from "geospatial dashboard".  The framework is built to be extremely extensible. You can use GeoDash server (an implementation), the front-end framework, backend code, or just the Gulp pipeline.

The `geonode.contrib.dashboards` contrib app is lightweigth.

You can learn more at the [Medium post](https://medium.com/@pjdufour.dev/introducing-geodash-18f1d68bd6f5#.47zrhm8dx).

## Installation

```
pip install -r geonode/contrib/dashboards/requirements.txt
python manage.py makemigrations geonode
python manage.py migrate geonode
```

## Settings

### Activation

To activate the GeoDash contrib app, you need to add `geonode.contrib.dashboards` to `INSTALLED_APPS`.  For example, with:

```Python
GEONODE_CONTRIB_APPS = (
    'geonode.contrib.dashboards'
)
GEONODE_APPS = GEONODE_APPS + GEONODE_CONTRIB_APPS
```

### Configuration

Once `dashboards` is added to `INSTALLED_APPS` (via `GEONODE_APPS`) in [settings.py](https://github.com/GeoNode/geonode/blob/master/geonode/settings.py) it will be active.
