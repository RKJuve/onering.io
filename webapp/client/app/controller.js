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
    this.user = new User();
    this.sms = new SMS();
    this.vm = new VM();
    this.all = new ALL();
    
    //initialize main layout view
    this.layout = new Layout();
    // show layout view
    this.region.show(this.layout);

    this.user.fetch({
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
    console.log('index');
    if (this.user.isNew()) {
      onering.masterRouter.navigate('signup',{trigger: true});
    } else {
      onering.masterRouter.navigate('home',{trigger: true});
    }
  },
  home: function() {
    if (this.user.isNew()) {
      onering.masterRouter.navigate('signup',{trigger: true});
    }
    this.layout.main.close();
    this.layout.main.show(new Dashboard());
    this.layout.navbar.show(new DefaultNav({model: this.user}))
    $('#navSettings').removeClass('active');
    $('#navDashboard').addClass('active');
  },
  signup: function() {
  	this.layout.main.show(new Signup());
    this.layout.navbar.show(new LoginNav());
  },
  getStarted: function() {
  	this.layout.main.show(new GetStarted());
  },
  settings: function() {
    this.layout.main.show(new Settings({model: this.user}))
    $('#navDashboard').removeClass('active');
    $('#navSettings').addClass('active');
  }
});
