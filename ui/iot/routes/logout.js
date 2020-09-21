module.exports = (function(){
	// var
	var request = require('request');

	// initialisation of variables

	// decalre functions
	function handleLogout(req, res){
		var userId = JSON.parse(req.userSession.user).id; 
		request.post({
			url:     `http://127.0.0.1:8080/logout?userId=${userId}`,
		  }, function(error, response, body){
			if (error) {
				console.error(error)
				return
			  }
			  console.log(`statusCode: ${response.statusCode}`)
			  req.userSession.IsAuthenticated = false;
			  req.userSession.IsAuthorised = false;
			  req.userSession.user = null;
			  req.userSession.bikeId = '';
		      req.userSession.mqqtPoints = null;
		  });

		

		res.send(req.userSession);
	}	

	// declare init
	function init(routeConfig){
		routeConfig.app.get('/logout', handleLogout);
	}

	// return
	return {
		init: init
	}
})();