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
				'profile.hbs'));
	}

	function handleProfileGet(req, res){
		var userId = JSON.parse(req.userSession.user).id;
		

		request.get({
			url:     `http://127.0.0.1:8080/getuser?userId=${userId}`
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

	function handleProfilePost(req, res){
		var userId = JSON.parse(req.userSession.user).id;
		
		data = req.body;
		data.userId = userId;

		request.post({
			headers: {'content-type' : 'application/json'},
			url:     `http://127.0.0.1:8080/editUser?userId=${userId}`,
			body:    JSON.stringify(data)
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
		routeConfig.app.get('/profile-template', handleProfileTemplate);
		routeConfig.app.get('/profile', handleProfileGet);
		routeConfig.app.post('/profile', handleProfilePost);
	}

	// return
	return {
		init: init
	}
})();