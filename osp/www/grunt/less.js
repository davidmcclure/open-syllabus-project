

module.exports = {

  options: {
    paths: 'node_modules'
  },

  ranks: {
    src: '<%= src.css %>/ranks/index.less',
    dest: '<%= dist %>/ranks.css',
  },

  text: {
    src: '<%= src.css %>/text/index.less',
    dest: '<%= dist %>/text.css',
  },

};
