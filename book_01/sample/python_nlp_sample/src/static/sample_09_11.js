var main = new Vue({
  el: '#main',
  data: {
    name:     'affiliation',
    keywords: 'インド',
    result:   {},
  },
  methods: {
    run: function() {
      this.$http.get(
        '/get',
        {'params': {
          'name':     this.name,
          'keywords': this.keywords,
        }},
      ).then(response => {
        this.result = response.body.response;
        console.log(this.result);
      }, response => {
        console.log('NG');
        console.log(response.body);
      });
    },
  }
});
