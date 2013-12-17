var Router = require('router'),
    Controller = require('controller');

var onering = new Backbone.Marionette.Application();

onering.addRegions({
    dropzone: '#dropzone'
    //body: 'body'
});

onering.addInitializer(function() {
    Swag.registerHelpers();
});

onering.addInitializer(function() {
    new Router({
        controller: new Controller({region: this.dropzone})
    });
});

onering.on('initialize:after', function() {
    Backbone.history.start();
});

module.exports = onering;
