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
				'currenttrip.hbs'));
	}

	function handleStartTrip(req, res){
		var bikeId = req.userSession.bikeId;
		var userId = JSON.parse(req.userSession.user).id;
		

		request.get({
			url:     `http://127.0.0.1:8080/getEndPoints?userId=${userId}&bikeId=${bikeId}`
		  }, function(error, response, body){
			if (error) {
				console.error(error)
				return
			  }
			  console.log(`statusCode: ${response.statusCode}`)
			  console.log(body)
			  if(body != null && body != ''){
				  	req.userSession.mqqtPoints = body
					res.send(req.userSession);
				}
				else {
				res.send(false);
				}
		  });

		
    }
    
    function handleEndTrip(req, res){
		var bikeId = req.userSession.bikeId;
		

		request.get({
			url:     `http://127.0.0.1:8080/endTrip?bikeId=${bikeId}`
		  }, function(error, response, body){
			if (error) {
				console.error(error)
				return
			  }
			  console.log(`statusCode: ${response.statusCode}`)
			  if(body != null && body != ''){
                    console.log(body)
					res.send(true);
				}
				else {
				res.send(false);
				}
		  });

		
	}

	// declare init
	function init(routeConfig){
		routeConfig.app.get('/currenttrip-template', handleProfileTemplate);
        routeConfig.app.get('/startTrip', handleStartTrip);
        routeConfig.app.get('/endTrip', handleEndTrip);
	}

	// return
	return {
		init: init
	}
})();