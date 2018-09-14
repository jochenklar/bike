(function(){

    Vue.component('bike-nav', {
        data: function() {
            return {
                active: null
            }
        },
        methods: {
            open: function(item) {
                if (this.active == item) {
                    this.active = null;
                } else {
                    this.active = item;
                }
            },
            close: function() {
                this.active = null;
            }
        }
    });

})();
