var store = (function(){

    function computePoint() {
        // distance.push(point[4]);
        // elevation.push({
        //     x: point[4],
        //     y: point[2]
        // });
        // velocity.push({
        //     x: point[4],
        //     y: point[5] * 3.6
        // });
    }

    var state = {
        tracks: null,
        track: null,
        focus: false
    };

    var methods = {
        fetchTracks: function() {
            return fetch('/tracks/')
                .then(function(response) {
                    return response.json();
                })
                .then(function(json) {
                    store.state.tracks = json;
                });
        },
        fetchTrack: function(track_id) {
            return fetch('/tracks/' + track_id + '/')
                .then(function(response) {
                    return response.json();
                })
                .then(function(json) {
                    var points = [];

                    json.features.forEach(function(feature) {
                        if (feature.geometry.type == 'LineString') {
                            feature.geometry.coordinates.forEach(function(point) {
                                points.push(point);
                            });
                        } else if (feature.geometry.type == 'MultiLineString') {
                            feature.geometry.coordinates.forEach(function(segment) {
                                segment.forEach(function(point) {
                                    points.push(point);
                                });
                            });
                        }
                    });

                    store.state.track = json;
                    store.state.track.points = points;
                });
        }
    };

    return {
        state: state,
        methods: methods
    };

})();
