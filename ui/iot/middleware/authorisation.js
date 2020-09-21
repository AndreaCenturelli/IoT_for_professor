module.exports = function(authInfo){
	return function(req, res, next){
		var currentUrl = req._parsedUrl.pathname.substring(1);
		
		if(currentUrl.indexOf("/") !== -1){
			currentUrl = currentUrl.substring(0, currentUrl.indexOf("/"));
		}

		var currentUrlKiAuthInfo = null;
		var i = 0;
		for(i = 0; i < authInfo.length; i++){
			if(authInfo[i].url === currentUrl){
				currentUrlKiAuthInfo = authInfo[i];
				break;
			}
		}

		if(currentUrlKiAuthInfo != null){
			var currentRole = req.userSession.user.Role;
			var foundAt = currentUrlKiAuthInfo.roles.indexOf(currentRole);

			if(foundAt == -1){
				req.userSession.IsAuthorised = false;
				res.send(req.userSession);
			} else {
				req.userSession.IsAuthorised = true;
				next();
			}
		}
		else {
			next();
		}

	}
}