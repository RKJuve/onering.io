var Layout = require('views/default'),
Signup = require('views/signup'),
GetStarted = require('views/get-started'),
LoginNav = require('views/loginNav'),
Dashboard = require('views/dashboard'),
DefaultNav = require('views/default-nav'),
Settings = require('views/settings'),
User = require('models/user'),
SMS = require('models/sms-collection'),
VM = require('models/vm-collection'),
ALL = require('models/all-collection');

module.exports = Backbone.Marionette.Controller.extend({
  initialize: function(options) {
    this.region = options.region;

    // initialize models/collections
    onering.user = new User();
    onering.sms = new SMS();
    onering.vm = new VM();
    onering.all = new ALL();
    
    //initialize main layout view
    this.layout = new Layout();
    // show layout view
    this.region.show(this.layout);

    onering.user.fetch({
      success: function(data) {
        console.log('-----user model synced from mongo below------')
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
    if (onering.user.isNew()) {
      onering.masterRouter.navigate('signup',{trigger: true});
    } else {
      onering.masterRouter.navigate('home',{trigger: true});
    }
  },
  home: function() {
    if (onering.user.isNew()) {
      onering.masterRouter.navigate('signup',{trigger: true});
    }
    this.layout.main.close();
    this.layout.main.show(new Dashboard());
    this.layout.navbar.show(new DefaultNav({model: onering.user}))
    $('#navSettings').removeClass('active');
    $('#navDashboard').addClass('active');
  },
  signup: function() {
  	this.layout.main.show(new Signup());
    this.layout.navbar.show(new LoginNav());
  },
  getStarted: function() {
    if (onering.user.isNew()) {
  	  this.layout.main.show(new GetStarted());
    } else {
      onering.masterRouter.navigate('home',{trigger: true});
    }
  },
  settings: function() {
    this.layout.main.show(new Settings({model: onering.user}))
    $('#navDashboard').removeClass('active');
    $('#navSettings').addClass('active');
  },
  welcome: function() {
    this.layout.main.show(new Dashboard());
  }
});
