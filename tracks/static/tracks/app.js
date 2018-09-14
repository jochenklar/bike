(function(){

    window.addEventListener("load", function(event) {

        var app = new Vue({
            el: '#app',
            data: store.state,
            methods: store.methods,
            delimiters: ['{$', '$}'],
            created: function () {
                this.fetchTracks();
            }
        });

    });

})();
