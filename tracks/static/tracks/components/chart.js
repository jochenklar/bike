(function(){

    Chart.defaults.bike = Chart.defaults.line;
    Chart.controllers.bike = Chart.controllers.line.extend({
        draw: function(ease) {
            Chart.controllers.line.prototype.draw.call(this, ease);

            if (this.chart.tooltip._active && this.chart.tooltip._active.length) {
                var activePoint = this.chart.tooltip._active[0],
                ctx = this.chart.ctx,
                x = activePoint.tooltipPosition().x,
                topY = this.chart.scales['y-axis-0'].top,
                bottomY = this.chart.scales['y-axis-0'].bottom;

                // draw line
                ctx.save();
                ctx.beginPath();
                ctx.moveTo(x, topY);
                ctx.lineTo(x, bottomY);
                ctx.lineWidth = 1;
                ctx.strokeStyle = 'silver';
                ctx.stroke();
                ctx.restore();
            }
        }
    });

    Vue.component('bike-profile', {
        template: '<div class="chart"><canvas id="chart"></canvas>',
        data: function() {
            return {
                chart: null
            }
        },
        props: {
            track: Object
        },
        watch: {
            track: function() {
                this.displayTrack();
            }
        },
        created: function() {

        },
        methods: {
            displayTrack: function() {
                if (this.chart != null) {
                    this.chart.destroy();
                }

                if (this.track != null) {

                    this.chart = new Chart(document.getElementById('chart'), {
                        type: 'bike',
                        responsive: true,
                        data: {
                            datasets: [
                                {
                                    label: 'Elevation',
                                    pointRadius: 0,
                                    borderColor: '#900',
                                    borderWidth: 2,
                                    fill: false,
                                    showPoint: false,
                                    yAxisID: 'y-axis-0',
                                    data: this.track.points.map(function(point) {
                                        return {
                                            x: point[4],
                                            y: point[2]
                                        }
                                    })
                                },
                                {
                                    label: 'Velocity',
                                    pointRadius: 0,
                                    pointHitRadius: 5,
                                    borderColor: '#009',
                                    borderWidth: 2,
                                    fill: false,
                                    showPoint: false,
                                    yAxisID: 'y-axis-1',
                                    data: this.track.points.map(function(point) {
                                        return {
                                            x: point[4],
                                            y: point[5] * 3.6
                                        }
                                    })
                                }
                            ]
                        },
                        options: {
                            maintainAspectRatio: false,
                            onHover: (function(event, array) {
                                if (this.chart.tooltip._active && this.chart.tooltip._active.length) {
                                    var activePoint = this.chart.tooltip._active[0];
                                    this.$emit('hover', activePoint._index);
                                }
                            }).bind(this),
                            legend: {
                                display: false
                            },
                            tooltips: {
                                enabled: false,
                                mode: 'index',
                                intersect: false
                            },
                            scales: {
                                xAxes: [{
                                    type: 'linear',
                                    display: true
                                }],
                                yAxes: [{
                                    type: 'linear',
                                    display: true,
                                    position: 'left',
                                    id: 'y-axis-0',
                                }, {
                                    type: 'linear',
                                    display: true,
                                    position: 'right',
                                    id: 'y-axis-1',
                                    gridLines: {
                                        drawOnChartArea: false
                                    },
                                }],
                            },
                            layout: {
                                padding: {
                                    left: 20,
                                    right: 20,
                                    top: 40,
                                    bottom: 20
                                }
                            }
                        }
                    });

                }
            }
        }
    });

})();
