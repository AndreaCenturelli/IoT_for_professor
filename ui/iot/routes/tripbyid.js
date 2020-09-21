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
				'tripbyid.hbs'));
	}

	function handleGetTrip(req, res){
		var data = req.body;
		var tripId = data.tripId;
		var userId = JSON.parse(req.userSession.user).id;
		

		request.get({
			url:     `http://127.0.0.1:8080/getTrip?userId=${userId}&tripId=${tripId}`
		  }, function(error, response, body){
			if (error) {
				console.error(error)
				return
			  }
			  console.log(`statusCode: ${response.statusCode}`)
			  console.log(body)
			  if(body != null && body != ''){
					res.send(body);
				}
				else {
				res.send(false);
				}
		  });

		
    }

	// declare init
	function init(routeConfig){
		routeConfig.app.get('/tripbyid-template', handleProfileTemplate);
        routeConfig.app.post('/getTrip', handleGetTrip);
	}

	// return
	return {
		init: init
	}
})();