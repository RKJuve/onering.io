var Layout = Backbone.Marionette.Layout.extend({
    template: require("./template"),
    regions: {
	    navbar: '#navbarRegion',
	    main: '#mainRegion',
	    footer: '#footerRegion',
	    modal: '#modalRegion'
	},
});

module.exports = Layout;
