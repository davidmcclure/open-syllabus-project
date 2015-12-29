

module.exports = function(grunt) {

  require('time-grunt')(grunt);
  require('jit-grunt')(grunt);

  require('load-grunt-config')(grunt, {

    loadGruntTasks: false,

    data: {
      js: 'static/src/javascripts',
      css: 'static/src/stylesheets',
      dist: 'static/dist'
    }

  });

};
