

module.exports = function(grunt) {

  require('time-grunt')(grunt);
  require('jit-grunt')(grunt);

  require('load-grunt-config')(grunt, {

    loadGruntTasks: false,

    data: {
      src: 'static/src',
      dest: 'static/dist',
    }

  });

};
