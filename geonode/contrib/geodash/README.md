# GeoDash Contrib App

GeoDash is a modern web framework and approach for quickly producing visualizations of geospatial data. The name comes from "geospatial dashboard".

The framework is built to be extremely extensible. You can use GeoDash server (an implementation), the front-end framework, backend code, or just the Gulp pipeline.

The `geonode.contrib.geodash` contrib app is a lighweight connector for GeoDash Server.

You can learn more at the [Medium post](https://medium.com/@pjdufour.dev/introducing-geodash-18f1d68bd6f5#.47zrhm8dx).

## Settings

### Activation

To activate the GeoDash contrib app, you need to add `geonode.contrib.geodash` to `INSTALLED_APPS`.  For example, with:

```Python
GEONODE_CONTRIB_APPS = (
    'geonode.contrib.geodash'
)
GEONODE_APPS = GEONODE_APPS + GEONODE_CONTRIB_APPS
```

### Configuration

Once GeoDash is added to `INSTALLED_APPS` (via `GEONODE_APPS`) in [settings.py](https://github.com/GeoNode/geonode/blob/master/geonode/settings.py) it will be active.
