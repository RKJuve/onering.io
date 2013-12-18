var Router = require('router'),
    Controller = require('controller');

var onering = new Backbone.Marionette.Application();

onering.addRegions({
    body: 'body'
});

onering.addInitializer(function() {
    Swag.registerHelpers();
});

onering.addInitializer(function() {

	// master router/controller
	onering.masterController = new Controller({region: this.body});
	onering.masterRouter = new Router({
		controller: onering.masterController
	});
});

onering.on('initialize:after', function() {
    Backbone.history.start();
});

module.exports = onering;
