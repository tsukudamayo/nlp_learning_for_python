var main = new Vue({
  el: '#main',
  data: {
    keywords:   '魚',
    result:     [],
    hl:         {},
  },
  methods: {
    run: function() {
      this.$http.get(
        '/get',
        {'params': {
          'keywords': this.keywords,
        }},
      ).then(response => {
        this.result = response.body.response;
        this.hl = response.body.highlighting;
      }, response => {
        console.log('NG');
        console.log(response.body);
      });
    },
  }
});
