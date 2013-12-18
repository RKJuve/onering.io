var Layout = require('views/default'),
	Signup = require('views/signup');

module.exports = Backbone.Marionette.Controller.extend({
    initialize: function(options) {
        this.region = options.region;
        this.layout = new Layout();
        this.region.show(this.layout);
    },

    // regions in the layout
    // this.layout.footer
    // this.layout.navbar
    // this.layout.main
    // this.layout.modal

    testRoute: function() {
    	this.layout.footer.show(new Signup());
    	this.layout.modal.show(new Signup());
    }
});
