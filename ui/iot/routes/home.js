module.exports = (function(){
	// var
	var path  = require('path');
	var pc = {};

	// initialisation of variables

	// decalre functions
	function handleProfileTemplate(req, res){
		res.sendFile(
			path.join(
				__dirname, 
				'..\\templates', 
				'home.hbs'));
	}


	// declare init
	function init(routeConfig){
		pc.config = routeConfig.dbConfig;
		routeConfig.app.get('/home-template', handleProfileTemplate);
	}

	// return
	return {
		init: init
	}
})();