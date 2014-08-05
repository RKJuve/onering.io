var GetStarted = Backbone.Marionette.ItemView.extend({
    template: require("./template"),
    events: {
    	'submit form': 'createAcct',
    	'click #formButton': 'createAcct'
    },
    createAcct: function() {
        var formFilled = true
        $(":text, number, email").each(function() {
            if($.trim($(this).val()) === '') {
                formFilled = false;  
            }
        });
        console.log('sanity');
        console.log(formFilled);

        if (formFilled) {
            var data = {
                email: $('#email').val(),
                firstname: $('#firstname').val(),
                lastname: $('#lastname').val(),
                auth_id: $('#auth_id').val(),
                auth_token: $('#auth_token').val(),
                plivoNumber: $('#plivoNumber').val()
            }   

            $.ajax({
                type: "POST",
                url:'/v1/user',
                data: JSON.stringify(data),
                headers: {
                    "Content-Type": "application/json"
                },
                success: function(data) {
                    onering.user.set(data);
                    onering.masterRouter.navigate('welcome', {trigger: true})
                }
            })
        } else {

        }
    }
});

module.exports = GetStarted;
