

module.exports = function(grunt) {

  require('time-grunt')(grunt);
  require('jit-grunt')(grunt);

  require('load-grunt-config')(grunt, {

    loadGruntTasks: false,

    data: {

      src: {
        js:  'assets/javascripts',
        css: 'assets/stylesheets',
      },

      dist: 'static/dist'

    }

  });

};
