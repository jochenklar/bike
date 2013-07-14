var current = {};
var leafletMap;

function displaymap() {
    var url = 'http://tiles.jochenklar.de/bbs/{z}/{x}/{y}.png';
    var opt = {
        'attribution': 'Map data © 2012 OpenStreetMap contributors | Style by <a href="http://buergerbautstadt.de" target="blank">buergerbautstadt.de</a>',
        'maxZoom': 18,
        'minZoom': 10
    }

    leafletMap = L.map('map').setView([52.51, 13.37628], 10);
    L.tileLayer(url, opt).addTo(leafletMap);
}

function displaytrack(id) {
    $.ajax({
        type: 'GET',
        url: '/tracks/' + id,
        dataType: 'json',
        headers: {
            Accept: 'application/json'
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        },
        success: function (json) {
            if (!$.isEmptyObject(current)) {
                leafletMap.removeLayer(current.track);
                current.meta.remove();
                current.info.remove();
            }

            // build info box
            current.info = $('<p/>',{
                'html': json.name + ' - ' + json.timestamp
            }).appendTo($('#info'))
            $('#info').show();

            // get metadata
            var meta = json.track.properties;

            // convert units
            var h = Math.floor(meta.time/3600);
            var m = Math.floor((meta.time%3600) / 60 );
            var s = Math.floor(meta.time%60);
            var dist = Math.round(meta.dist) / 1000;
            var speed = Math.round(meta.speed  * 1.609344 * 100) / 100;

            // build meta box
            html = '<tr><td>Gesamtzeit:&nbsp;</td>'
            html += '<td>'+h+':'+m+':'+s+' h</td></tr>';
            html += '<tr><td>Entfernung:&nbsp;</td>';
            html += '<td>'+dist+' km</td></tr>';
            html += '<tr><td>&#216; Geschwindigkeit:&nbsp;</td>';
            html += '<td>'+speed+' km/h</td></tr>';
            html += '<tr><td>&#216; Trittfrequenz:&nbsp;</td>';
            html += '<td>'+meta.cad+'</td></tr>';
            html += '<tr><td>Kalorien:&nbsp;</td>';
            html += '<td>'+meta.cal+'</td></tr>';
            current.meta = $('<table/>',{
                'html': html
            }).appendTo($('#meta'))
            $('#meta').show();
            
            // get tackpoint array
            tp = json.track.geometry.coordinates[0]

            // build track box
            var data = [];
            for (var i = 0; i < tp.length; i++ ) {
                data.push([tp[i][2],tp[i][3]]);
            }
            var series = {
                data: data,
                color: '#0078A8',
                clickable: true
            }
            var plotoptions = {
                grid: {
                    'color': '#ccc'
                }
            };
            var plot = $.plot('#track', [series], plotoptions);
            $('#track').show();

            // display track in map
            current.track = L.geoJson(json.track, {
                style : {
                    "color": '#0078A8',
                    "weight": 3,
                    "opacity": 0.75
                }
            }).addTo(leafletMap);
        }
    });
}

function init() {
    displaymap();

    var trackid = window.location.hash.substring(1);
    if (trackid.length != 0 && trackid % 1 === 0) {
        // trackid is a number, so lets display the track
        displaytrack(trackid);
    }

    $('.load-track').bind('click', function(event) {
        // display the track on menu click
        displaytrack(this.href.split('#')[1]);
    });
}
