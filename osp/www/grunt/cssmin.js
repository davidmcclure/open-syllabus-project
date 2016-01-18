

module.exports = {

  dist: {
    files: [{
      expand: true,
      cwd: '<%= dist %>',
      dest: '<%= dist %>',
      src: '*.css',
    }]
  },

};
