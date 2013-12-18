var Layout = require('views/default'),
	Signup = require('views/signup'),
	GetStarted = require('views/get-started'),
    LoginNav = require('views/loginNav'),
    Dashboard = require('views/dashboard')
    User = require('models/user');

module.exports = Backbone.Marionette.Controller.extend({
    initialize: function(options) {
        this.region = options.region;
        this.layout = new Layout();
        this.user = new User();
        this.region.show(this.layout);
        this.user.fetch({
            success: function(data) {
                console.log(data);
                onering.masterRouter.navigate('home',{trigger: true});
            },
            error: function() {
                onering.masterRouter.navigate('signup',{trigger: true});
            }
        });
    },
    // regions in the layout
    // this.layout.footer
    // this.layout.navbar
    // this.layout.main
    // this.layout.modal
    index: function() {
        this.layout.main.close();
    },
    home: function() {
        this.layout.main.close();
        this.layout.main.show(new Dashboard());
    },
    signup: function() {
    	this.layout.main.show(new Signup());
        this.layout.navbar.show(new LoginNav());
    },
    getStarted: function() {
    	this.layout.main.show(new GetStarted());
    }
});
