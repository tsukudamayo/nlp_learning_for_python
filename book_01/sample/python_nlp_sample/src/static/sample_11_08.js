var main = new Vue({
  el: '#main',
  data: {
    title:    'シンガポール',
    keywords: '教育',
    result:   {},
  },
  methods: {
    run: function() {
      this.$http.get(
        '/get',
        {'params': {
          'title':      this.title,
          'keywords':   this.keywords,
        }},
      ).then(response => {
        this.result = response.body.response;
      }, response => {
        console.log('NG');
        console.log(response.body);
      });
    },
  }
});

