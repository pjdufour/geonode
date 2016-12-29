var dashboards = {
  "bootloader": {
    "loaders": {}
  },
  "search": {
    "codec": {},
    "datasets": {}
  }
};


dashboards.search.codec.GeoNodeDashboards = function(response, url)
{
  var encoded = [];

  var dashboards = response.objects;
  for(var i = 0; i < dashboards.length; i++)
  {
    var dashboard = dashboards[i];
    var id = dashboard.uuid;
    var title = dashboard.title;
    var x = {
      'id': id,
      'text': title,
    };
    encoded.push(x);
  }

  return encoded;
};

dashboards.search.codec.GeoNodeProfiles = function(response, url)
{
  var encoded = [];

  var profiles = response.objects;
  for(var i = 0; i < profiles.length; i++)
  {
    var profile = profiles[i];
    var id = profile.username;
    var title = profile.username;
    var x = {
      'id': id,
      'text': title,
      'obj': profile
    };
    encoded.push(x);
  }

  return encoded;
};


dashboards.search.datasets.GeoNodeDashboards = function(element, featurelayers, baselayers, servers, codecs)
{
  var datasets = [];
  var template_suggestion = extract(element.data('template-suggestion') || 'default', geodash.typeahead.templates.suggestion);
  var url = geodash.api.getEndpoint("GEONODE_DASHBOARDS");
  var local = undefined;
  var prefetchOptions = {
    url: url,
    dataType: 'json',
    codec: "GeoNodeDashboards",
    cache: false,
    codecs: codecs
  };
  var prefetch = geodash.bloodhound.prefetch(prefetchOptions);
  var engine = geodash.bloodhound.engine({ "prefetch": prefetch });
  var templates = { suggestion: template_suggestion };
  var dataset = {
    name: "dashboards",
    engine: engine,
    minLength: 0,
    limit: 10,
    hint: false,
    highlight: true,
    display: geodash.typeahead.displayFn,
    source: function (query, syncResults, asyncResults) { this.engine.ttAdapter()(query, syncResults, asyncResults); },
    templates: templates
  };
  datasets.push(dataset);

  return datasets;
};

dashboards.search.datasets.GeoNodeProfiles = function(element, featurelayers, baselayers, servers, codecs)
{
  var datasets = [];
  var template_suggestion = extract(element.data('template-suggestion') || 'default', geodash.typeahead.templates.suggestion);
  var url = geodash.api.getEndpoint("GEONODE_PROFILES");
  var local = undefined;
  var prefetchOptions = {
    url: url,
    dataType: 'json',
    codec: "GeoNodeProfiles",
    cache: false,
    codecs: codecs
  };
  var prefetch = geodash.bloodhound.prefetch(prefetchOptions);
  var engine = geodash.bloodhound.engine({ "prefetch": prefetch });
  var templates = { suggestion: template_suggestion };
  var dataset = {
    name: "profiles",
    engine: engine,
    minLength: 0,
    limit: 10,
    hint: false,
    highlight: true,
    display: geodash.typeahead.displayFn,
    source: function (query, syncResults, asyncResults) { this.engine.ttAdapter()(query, syncResults, asyncResults); },
    templates: templates
  };
  datasets.push(dataset);

  return datasets;
};
