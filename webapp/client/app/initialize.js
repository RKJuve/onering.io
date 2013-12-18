// initialize new application after DOM has fully loaded

var onering = window.onering = require('application');

$(function() {
	console.log(onering);
    // app.initialize();
    onering.start();
});
