var Layout = require('views/default');

module.exports = Backbone.Marionette.Controller.extend({
    initialize: function(options) {
        this.region = options.region;
    },

    showHome: function() {
        this.region.show(new Layout());
    }
});
