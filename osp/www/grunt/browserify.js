

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

      'yamlify',

    ],

    watch: true,

    browserifyOptions: {
      debug: true
    },

  },

  ranks: {
    src: '<%= src.js %>/ranks/index.js',
    dest: '<%= dist %>/ranks.js',
  },

  graph: {
    src: '<%= src.js %>/graph/index.js',
    dest: '<%= dist %>/graph.js',
  },

};
