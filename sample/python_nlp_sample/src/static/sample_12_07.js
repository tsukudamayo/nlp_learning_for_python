var main = new Vue({
  el: '#main',
  data: {
    name:     'cause',
    keywords:       '',
    anno_names_str: 'cause effect',
    anno_names:     [],
    result:   {},
  },
  methods: {
    run: function() {
      this.anno_names = this.anno_names_str.split(/\s+/);
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
