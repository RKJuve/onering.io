var LoginSwitch = Backbone.Marionette.ItemView.extend({
    template: require("./template"),
    events: {
		'click #loginSwitch': 'loginSwitch'
	},
	loginSwitch: function(){
		if (this.model.get('loginState') === true) {
			this.model.set('loginState', false);
			$('#loginSwitch').removeClass('btn-success').addClass('btn-warning');
			$('#loginSwitch').html('not logged in');
		} else {
			console.log(this.model);
			this.model.set('loginState', true);
			$('#loginSwitch').removeClass('btn-warning').addClass('btn-success');
			$('#loginSwitch').html('logged in');
		}

	}
});

module.exports = LoginSwitch;