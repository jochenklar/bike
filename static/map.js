var _leafletMap, _currentTrack, _tiles_url, _tiles_opt, _track_color;

function init() {
    Handlebars.registerHelper("prettifyDate", function(timestamp) {
        return moment(new Date(timestamp)).format('ll');
    });

    displayNavigation();
    displayMap();

    var trackid = window.location.hash.substring(1);
    if (trackid.length !== 0 && trackid % 1 === 0) {
        // trackid is a number, so lets display the track
        displayTrack(trackid);
    }
}

function displayMap() {
    _leafletMap = L.map('map').setView([52.51, 13.37628], 12);
    L.tileLayer(_tiles_url, _tiles_opt).addTo(_leafletMap);
}

function displayNavigation() {
    $.ajax({
        url: '/tracks/',
        success: function (data) {
            var template = Handlebars.compile($("#navigation-template").html());
            var html     = template({'data': data});
            $('#navigation').append(html);

            $('.load-track').bind('click', function(event) {
                // display the track on menu click
                displayTrack(this.href.split('#')[1]);
            });
        }
    });
}

function displayTrack(id) {
    $.ajax({
        url: '/tracks/' + id,
        dataType: 'json',
        success: function (json) {
            if (json.type === 'FeatureCollection') {
                json = json.features[0];
            }

            var trackpoints;
            if (json.geometry.type === 'MultiLineString') {
                trackpoints = json.geometry.coordinates[0];
            } else {
                trackpoints = json.geometry.coordinates;
            }

            displayProperties(json.properties);
            displayProfiles(trackpoints);

            // display track on leaflet map
            if (typeof _currentTrack !== 'undefined') {
                _leafletMap.removeLayer(_currentTrack);
            }
            _currentTrack = L.geoJson(json, {
                style : {
                    "color": _track_color,
                    "weight": 5,
                    "opacity": 0.75
                }
            }).addTo(_leafletMap);

            _leafletMap.panTo(new L.LatLng(trackpoints[0][1], trackpoints[0][0]));
        }
    });
}

function displayProperties(properties) {
    $('#properties').empty();

    var template_config = {};

    if (typeof properties != 'undefined') {
        if (typeof properties.total_time != 'undefined') {
            template_config.total_time = {
                'hours': Math.floor(properties.total_time/3600),
                'minutes': Math.floor((properties.total_time%3600) / 60 ),
                'seconds': Math.floor(properties.total_time%60)
            };
        }

        if (typeof properties.total_time != 'undefined') {
            template_config.total_dist = Math.round(properties.total_dist) / 1000;
        }

        if (typeof properties.total_time != 'undefined') {
            template_config.mean_speed = Math.round(properties.mean_speed * 360) / 100;
        }

        if (typeof properties.total_time != 'undefined') {
            template_config.maximum_speed = Math.round(properties.maximum_speed * 360) / 100;
        }

        if (typeof properties.total_time != 'undefined') {
            template_config.mean_cad = Math.round(properties.mean_cad * 100) / 100;
        }

        if (typeof properties.total_time != 'undefined') {
            template_config.maximum_cad = Math.round(properties.maximum_cad * 100) / 100;
        }
    }

    if (!$.isEmptyObject(template_config)) {
        var template = Handlebars.compile($("#properties-template").html());
        var html = template(template_config);
        $('#properties').append(html);
    }
}

function displayProfiles(trackpoints) {
    $('#profiles').empty();

    if (trackpoints[0].length > 2) {
        var template = Handlebars.compile($("#profiles-template").html());

        var html = template();

        $('#profiles').append(html);

        var m = [20, 80, 20, 80]; // margins
        var w = 800 - m[1] - m[3]; // width
        var h = 400 - m[0] - m[2]; // height

        trackpoints_t = d3.transpose(trackpoints);

        var x  = d3.scale.linear().domain([
            d3.min(trackpoints_t[4]) * 0.001,
            d3.max(trackpoints_t[4]) * 0.001
        ]).range([0, w]);
        var y1 = d3.scale.linear().domain([
            d3.min(trackpoints_t[2]),
            d3.max(trackpoints_t[2])
        ]).range([h, 0]);
        var y2 = d3.scale.linear().domain([
            d3.min(trackpoints_t[5]) * 3.6,
            d3.max(trackpoints_t[5]) * 3.6
        ]).range([h, 0]);

        var line1 = d3.svg.line()
            .x(function(d) {return x(d[4] * 0.001);})
            .y(function(d) {return y1(d[2]);});

        var line2 = d3.svg.line()
            .x(function(d) {return x(d[4] * 0.001);})
            .y(function(d) {return y2(d[5] * 3.6);});

        var graph = d3.select("#profiles-canvas").append("svg:svg")
            .attr("width", w + m[1] + m[3])
            .attr("height", h + m[0] + m[2])
            .append("svg:g")
                .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

        var xAxis = d3.svg.axis().scale(x).ticks(10);
        graph.append("svg:g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + h + ")")
            .call(xAxis);

        var yAxisLeft = d3.svg.axis().scale(y1).ticks(6).orient("left");
        graph.append("svg:g")
            .attr("class", "y axis axisLeft")
            .call(yAxisLeft);

        var yAxisRight = d3.svg.axis().scale(y2).ticks(6).orient("right");
        graph.append("svg:g")
            .attr("class", "y axis axisRight")
            .attr("transform", "translate(" + w + ",0)")
            .call(yAxisRight);

        graph.append("svg:path").attr("d", line1(trackpoints)).attr("class", "y1");
        graph.append("svg:path").attr("d", line2(trackpoints)).attr("class", "y2");
    }
}
