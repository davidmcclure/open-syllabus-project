

module.exports = {

  options: {

    transform: [

      ['babelify', {
        presets: ['es2015', 'stage-1']
      }],

    ],

    watch: true,

    browserifyOptions: {
      debug: true
    },

  },

  ranks: {
    src: '<%= js %>/ranks/index.js',
    dest: '<%= dist %>/ranks.js'
  }

};
