var Layout = require('views/default'),
	Signup = require('views/signup'),
	GetStarted = require('views/get-started'),
    LoginSwitch = require('views/login-switch'),
    User = require('models/user');

module.exports = Backbone.Marionette.Controller.extend({
    initialize: function(options) {
        this.region = options.region;
        this.layout = new Layout();
        this.region.show(this.layout);
        this.layout.navbar.show(new LoginSwitch({model:new User()}))
    },
    // regions in the layout
    // this.layout.footer
    // this.layout.navbar
    // this.layout.main
    // this.layout.modal
    home: function() {
        this.layout.main.close();
    },
    signup: function() {
    	this.layout.main.show(new Signup());
    },
    getStarted: function() {
    	this.layout.main.show(new GetStarted());
    }
});
