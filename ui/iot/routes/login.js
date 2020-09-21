module.exports = (function(){
	// var
	var path  = require('path');
	var request = require('request');

	// initialisation of variables

	// decalre functions
	function handleLoginTemplate(req, res){
		res.sendFile(
			path.join(
				__dirname, 
				'..\\templates', 
				'login.hbs'));
	}

	function handleLoginPost(req, res){
		var data = req.body;
		password = data.password
		email = data.email
		

		request.post({
			headers: {'content-type' : 'application/json'},
			url:     'http://127.0.0.1:8080/login',
			body:    JSON.stringify(data)
		  }, function(error, response, body){
			if (error) {
				console.error(error)
				return
			  }
			  console.log(`statusCode: ${response.statusCode}`)
			  console.log(body)
			  if(body != null && body != ''){

				req.userSession.IsAuthenticated = true;
				req.userSession.IsAuthorised = false;
				req.userSession.user = body;
				
				res.send(req.userSession);
				}
				else {
				req.userSession.IsAuthenticated = false;
				req.userSession.IsAuthorised = false;
				req.userSession.user = null;

				res.send(false);
				}
		  });

		
	}

	// declare init
	function init(routeConfig){
		routeConfig.app.get('/login-template', handleLoginTemplate);
		routeConfig.app.post('/login', handleLoginPost);
	}

	// return
	return {
		init: init
	}
})();