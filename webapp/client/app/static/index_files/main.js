(function(/*! Brunch !*/) {
  'use strict';

  var globals = typeof window !== 'undefined' ? window : global;
  if (typeof globals.require === 'function') return;

  var modules = {};
  var cache = {};

  var has = function(object, name) {
    return ({}).hasOwnProperty.call(object, name);
  };

  var expand = function(root, name) {
    var results = [], parts, part;
    if (/^\.\.?(\/|$)/.test(name)) {
      parts = [root, name].join('/').split('/');
    } else {
      parts = name.split('/');
    }
    for (var i = 0, length = parts.length; i < length; i++) {
      part = parts[i];
      if (part === '..') {
        results.pop();
      } else if (part !== '.' && part !== '') {
        results.push(part);
      }
    }
    return results.join('/');
  };

  var dirname = function(path) {
    return path.split('/').slice(0, -1).join('/');
  };

  var localRequire = function(path) {
    return function(name) {
      var dir = dirname(path);
      var absolute = expand(dir, name);
      return globals.require(absolute, path);
    };
  };

  var initModule = function(name, definition) {
    var module = {id: name, exports: {}};
    cache[name] = module;
    definition(module.exports, localRequire(name), module);
    return module.exports;
  };

  var require = function(name, loaderPath) {
    var path = expand(name, '.');
    if (loaderPath == null) loaderPath = '/';

    if (has(cache, path)) return cache[path].exports;
    if (has(modules, path)) return initModule(path, modules[path]);

    var dirIndex = expand(path, './index');
    if (has(cache, dirIndex)) return cache[dirIndex].exports;
    if (has(modules, dirIndex)) return initModule(dirIndex, modules[dirIndex]);

    throw new Error('Cannot find module "' + name + '" from '+ '"' + loaderPath + '"');
  };

  var define = function(bundle, fn) {
    if (typeof bundle === 'object') {
      for (var key in bundle) {
        if (has(bundle, key)) {
          modules[key] = bundle[key];
        }
      }
    } else {
      modules[bundle] = fn;
    }
  };

  var list = function() {
    var result = [];
    for (var item in modules) {
      if (has(modules, item)) {
        result.push(item);
      }
    }
    return result;
  };

  globals.require = require;
  globals.require.define = define;
  globals.require.register = define;
  globals.require.list = list;
  globals.require.brunch = true;
})();
require.register("application", function(exports, require, module) {
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

});

;require.register("controller", function(exports, require, module) {
var Layout = require('views/default'),
	Signup = require('views/signup'),
	GetStarted = require('views/get-started');

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
    home: function() {
    	console.log(this.layout);
    	this.layout.main.close();
    },
    signup: function() {
    	this.layout.main.show(new Signup());
    },
    getStarted: function() {
    	this.layout.main.show(new GetStarted());
    }
});

});

;require.register("initialize", function(exports, require, module) {
// initialize new application after DOM has fully loaded

var onering = require('application');

$(function() {
	var loginstate = [];
    // app.initialize();
    onering.start();
});

});

;require.register("router", function(exports, require, module) {
module.exports = Backbone.Marionette.AppRouter.extend({
    appRoutes: {
    	'': 'home',
    	'getstarted': 'getStarted',
    	'signup':'signup',
    	'home': 'home'

    }
});

});

;require.register("views/default/index", function(exports, require, module) {
var Layout = Backbone.Marionette.Layout.extend({
    template: require("./template"),
    regions: {
	    navbar: '#navbarRegion',
	    main: '#mainRegion',
	    footer: '#footerRegion',
	    modal: '#modalRegion'
	}
});

module.exports = Layout;

});

;require.register("views/default/template", function(exports, require, module) {
var __templateData = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<!-- static top navbar -->\n<div class=\"navbar navbar-inverse navbar-static-top\" role=\"navigation\">\n  <div class=\"container\">\n    <a class=\"navbar-brand\" href=\"#\">onering.io</a>\n\n    <!-- rendering region for navbar views -->\n    <ul id=\"navbarRegion\" class=\"nav navbar-nav\">\n  \n\n    </ul>\n    <ul class=\"nav navbar-nav navbar-right\">\n  \n    <button type=\"button\" id=\"loginSwitch\" class=\"btn btn-warning\">not logged in</button>\n\n    </ul>\n  </div>\n</div>\n\n<div id=\"wrap\">\n  <!-- main container and rendering region -->\n  <div id=\"mainRegion\" class=\"container\">\n  \n  </div>\n\n</div>\n\n<!-- footer with rendering region -->\n<footer class=\"footer\">\n  <div id=\"footerRegion\" class=\"container\">\n    \n  </div>\n</footer>\n\n<!-- modal with rendering region -->\n<div id=\"oneModal\" class=\"modal fade\">\n  <div class=\"modal-dialog\">\n  <div id=\"modalRegion\" class=\"modal-content\">\n      <div class=\"modal-header\">\n        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-hidden=\"true\">&times;</button>\n        <h4 class=\"modal-title\">One Modal</h4>\n      </div>\n      <div class=\"modal-body\">\n        <p>to bind them all!&hellip;</p>\n      </div>\n      <div class=\"modal-footer\">\n        <button type=\"button\" class=\"btn btn-default\" data-dismiss=\"modal\">Close</button>\n        <button type=\"button\" class=\"btn btn-primary\">Save changes</button>\n      </div>\n    </div><!-- /.modal-content -->\n  </div><!-- /.modal-dialog -->\n</div><!-- /.modal -->\n";
  });
if (typeof define === 'function' && define.amd) {
  define([], function() {
    return __templateData;
  });
} else if (typeof module === 'object' && module && module.exports) {
  module.exports = __templateData;
} else {
  __templateData;
}
});

;require.register("views/get-started/index", function(exports, require, module) {
var GetStarted = Backbone.Marionette.ItemView.extend({
    template: require("./template"),
});

module.exports = GetStarted;

});

;require.register("views/get-started/template", function(exports, require, module) {
var __templateData = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div class=\"panel panel-default\">\n  <div class=\"panel-heading\">\n    <h3 class=\"panel-title\">Step 1: Sign up for a free Plivo account</h3>\n  </div>\n  <div class=\"panel-body\">\n    Head over to <a href=\"http://plivo.com/\" target=\"_blank\">plivo.com</a> and sign up for an account.\n  </div>\n</div>\n\n<div class=\"panel panel-default\">\n  <div class=\"panel-heading\">\n    <h3 class=\"panel-title\">Step 2: Confirm your Plivo account</h3>\n  </div>\n  <div class=\"panel-body\">\n    You'll need to confirm your account with Plivo by clicking the link in the activation email they send you.  Once you've logged in for the first time, you should be prompted to confirm your cell phone number.  Plivo will call your cell phone with an activation code.\n  </div>\n</div>\n\n<div class=\"panel panel-default\">\n  <div class=\"panel-heading\">\n    <h3 class=\"panel-title\">Step 3: Sign up with onering.io</h3>\n  </div>\n  <div class=\"panel-body\">\n    We will need your Plivo Auth ID and Auth Token to communicate with Plivo's servers on your behalf. \n  </div>\n</div>";
  });
if (typeof define === 'function' && define.amd) {
  define([], function() {
    return __templateData;
  });
} else if (typeof module === 'object' && module && module.exports) {
  module.exports = __templateData;
} else {
  __templateData;
}
});

;require.register("views/signup/index", function(exports, require, module) {
var Signup = Backbone.Marionette.ItemView.extend({
    template: require("./template"),
});

module.exports = Signup;

});

;require.register("views/signup/template", function(exports, require, module) {
var __templateData = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div class=\"jumbotron\">\n	<h1>Welcome to onering.io</h1>\n	<p>One ring to bring them all, and in the cloudness bind them...</p>\n	<p>\n		<button class=\"btn btn-primary\" data-toggle=\"modal\" data-target=\"#oneModal\">\n			What is onering.io?\n		</button>\n		<a href=\"#getstarted\"><button class=\"btn btn-primary\">\n			Get Started\n		</button></a>\n	</p>	\n</div>";
  });
if (typeof define === 'function' && define.amd) {
  define([], function() {
    return __templateData;
  });
} else if (typeof module === 'object' && module && module.exports) {
  module.exports = __templateData;
} else {
  __templateData;
}
});

;
//# sourceMappingURL=main.js.map