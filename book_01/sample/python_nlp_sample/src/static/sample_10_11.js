var main = new Vue({
    el: '#main',
    data: {
        classifier: 'ml',
        keywords:   '麦',
        result:     {},
    },
    methods: {
        run: function() {
            this.$http.get(
                '/get',
                {'params': {
                    'keywords':   this.keywords,
                    'classifier': this.classifier,
                }},
            ).then(response => {
                console.log("OK");
                console.log(response.body);
                this.result = response.body.response;
            }, response => {
                console.log('NG');
                console.log(response.body);
            });
        },
    }
});
