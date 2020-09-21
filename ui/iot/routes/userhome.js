module.exports = (function(){
	// var
	var path  = require('path');
	var request = require('request');

	// initialisation of variables

	// decalre functions
	function handleProfileTemplate(req, res){
		res.sendFile(
			path.join(
				__dirname, 
				'..\\templates', 
				'userhome.hbs'));
	}


	// declare init
	function init(routeConfig){
		routeConfig.app.get('/userhome-template', handleProfileTemplate);
	}

	// return
	return {
		init: init
	}
})();