(function(){

    Vue.component('bike-map', {
        template: '<div id="map" class="map"></div>',
        data: function() {
            return {
                map: null,
                marker: null,
                layers: {}
            }
        },
        props: {
            url: String,
            attribution: String,
            minZoom: Number,
            maxZoom: Number,
            track: Object,
            focus: Number
        },
        watch: {
            track: function() {
                this.displayTrack();
            },
            focus: function(oldIndex, newIndex) {
                this.highlightPoint(oldIndex, newIndex);
            }
        },
        methods: {
            displayTrack: function() {
                if (this.layers.track) {
                    this.map.removeLayer(this.layers.track);
                    this.map.removeLayer(this.layers.highlight);
                }

                this.layers.track = L.geoJSON(this.track, {
                    style : {
                        color: '#900',
                        weight: 3
                    }
                });
                this.layers.highlight = L.geoJSON(this.track, {
                    style : {
                        color: '#fff',
                        weight: 5
                    }
                });

                this.map.flyToBounds(this.layers.track.getBounds());
                this.map.once('moveend', (function() {
                    this.layers.track.addTo(this.map);
                    this.layers.highlight.addTo(this.map);
                    this.layers.highlight.bringToBack();
                }).bind(this));
            },
            highlightPoint: function(oldIndex, newIndex) {
                if (this.marker != null) {
                    this.map.removeLayer(this.marker)
                }

                var point = this.track.points[newIndex];
                if (point !== undefined) {
                    this.marker = L.circleMarker([point[1], point[0]], {
                        color: '#fff',
                        fillColor: '#900',
                        fillOpacity: 1,
                        radius: 5
                    }).addTo(this.map);
                }
            }
        },
        mounted () {
            this.map = L.map('map').setView([52.518611, 13.408333], 10);
            this.layers.tiles = L.tileLayer(this.url, {
                'attribution': this.attribution,
                'minZoom': this.minZoom,
                'maxZoom': this.maxZoom
            }).addTo(this.map);
        }
    });

})();
