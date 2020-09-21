module.exports = (function(){
	// var
	var home = require('./home');
	var userhome = require('./userhome');
	var qr_scanner = require('./qr_scanner');
	var previoustrips = require('./previoustrips');
	var register = require('./register');
	var currenttrip = require('./currenttrip');
	var login = require('./login');
	var logout = require('./logout');
	var initR = require('./initR');
	var tripbyid = require('./tripbyid');
	var profile = require('./profile');

	// initialisation of variables

	// decalre functions

	// declare init
	function init(routeConfig){
		console.log("inside");
		home.init(routeConfig);
		userhome.init(routeConfig);
		qr_scanner.init(routeConfig);
		previoustrips.init(routeConfig);
		register.init(routeConfig);
		login.init(routeConfig);
		logout.init(routeConfig);
		initR.init(routeConfig);
		currenttrip.init(routeConfig);
		tripbyid.init(routeConfig);
		profile.init(routeConfig);
	}

	// return

	return {
		init: init
	}
})();