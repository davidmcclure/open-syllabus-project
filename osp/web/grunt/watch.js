

module.exports = {

  livereload: {
    files: '<%= dist %>/*',
    options: { livereload: true }
  },

  stylesheets: {
    files: '<%= css %>/**/*.less',
    tasks: 'less'
  }

};
