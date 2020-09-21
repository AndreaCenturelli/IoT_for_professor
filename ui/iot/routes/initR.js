module.exports = (function(){
	// var

	// initialisation of variables

	// decalre functions
	function handleGet(req, res){
		//console.log('5');
		res.send(req.userSession);
	}

	// declare init
	function init(routeConfig){
		//console.log('6');
		routeConfig.app.get('/init', handleGet);
	}

	// return
	return {
		init: init
	}
})();