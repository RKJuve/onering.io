var Dashboard = Backbone.Marionette.Layout.extend({
    template: require("./template"),
    regions: {
    	sms: '#smsRegion',
    	vm: "#vmRegion",
    	both: "#bothRegion"
    }
});

module.exports = Dashboard;