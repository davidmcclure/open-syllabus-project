

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
    src: '<%= src %>/javascripts/ranks/index.js',
    dest: '<%= dest %>/ranks.js'
  }

};