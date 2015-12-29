

module.exports = {

  livereload: {
    files: '<%= dest %>/*',
    options: { livereload: true }
  },

  stylesheets: {
    files: '<%= src %>/stylesheets/**/*.less',
    tasks: 'less'
  }

};
