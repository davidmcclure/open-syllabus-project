

module.exports = {

  options: {

    transform: [

      ['babelify', {

        presets: [
          'es2015',
          'stage-1',
          'react',
        ],

        // TODO: Until Babel 6 adds decorators.
        plugins:[
          'babel-plugin-transform-decorators-legacy',
        ]

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
