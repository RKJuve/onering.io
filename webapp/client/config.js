exports.config = {
  conventions: {
    assets: /^app[\\/]static/
  },
  paths: {
    "public": '../build'
  },
  files: {
    javascripts: {
      defaultExtension: 'js',
      joinTo: {
        'js/main.js': /^app/,
        'js/html5shiv.js': /^bower_components[\\/](?=html5shiv)/,
        'js/vendor.js': /^bower_components[\\/](?!html5shiv)/,
      },
      order: {
        before: [
          'bower_components/lodash/dist/lodash.underscore.js',
          'bower_components/jquery/jquery.js',
          'bower_components/backbone/backbone.js',
          'bower_components/marionette/lib/core/backbone.marionette.js',
          'bower_components/bootstrap/dist/js/bootstrap.min.js'
        ]
      }
    },
    stylesheets: {
      defaltExtension: 'css',
      joinTo: 'css/main.css',
      order: {
        before: [
          'bower_components/bootstrap/dist/css/bootstrap.css',
          'bower_components/bootstrap/dist/css/bootstrap-theme.css'
        ]
      }
    },
    templates: {
      defaultExtension: 'hbs',
      joinTo: 'js/main.js'
    }
  },
  framework: 'backbone'
};
