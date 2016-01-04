

module.exports = {

  livereload: {
    files: [
      '<%= dist %>/*',
      'templates/*',
    ],
    options: { livereload: true }
  },

  stylesheets: {
    files: '<%= src.css %>/**/*.less',
    tasks: 'less'
  }

};
