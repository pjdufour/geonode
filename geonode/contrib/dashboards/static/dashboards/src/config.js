geodash.config = {
  "bootloader": {
    "loaders": [dashboards.bootloader.loaders, geodash.bootloader.loaders]
  },
  "click_radius": 2.0,
  "search": {
    "datasets": [dashboards.search.datasets, geodash.typeahead.datasets],
    "codecs": [dashboards.search.codec, geodash.bloodhound.codec]
  },
  "dynamicStyleFunctionWorkspaces": [
    geodash.dynamicStyleFn
  ],
  "transport" : {
    "littleEndian": false
  },
  "popup": {
    "height": "309px",
    "context": {
      "e": extract,
      "extract": extract,
      "extractFloat": extractFloat
    },
    "listeners": {
      "show": []
    }
  },
  "whitelist": {
    "config": [
      "localhost",
      "127.0.0.1",
      "gist.githubusercontent.com",
      "geonode.wfp.org"
    ]
  }
};
