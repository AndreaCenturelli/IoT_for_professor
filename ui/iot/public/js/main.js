(function(){
	// var
	var $bodyContent;
	var $liUser, $liLogout, $liLogin;
	window.isAdminv;
	// var init
	$bodyContent = $('#bodyContent');
	$liUser = $('#liUser');
	$liLogout = $('#liLogout');
	$liLogin = $('#liLogin');

	// functions
	function handleHashChange(){
		debugger;
		switch(window.location.hash){
			case '#trips':
				window.trips.handleHash(injectBodyContent);
				break;
			case '#home':
				window.home.handleHash(injectBodyContent);
				break;
			case '#userhome':
				window.userhome.handleHash(injectBodyContent);
				break;
			case '#login':
				window.login.handleHash(injectBodyContent);
				break;
			case '#logout':
				window.logout.handleHash(injectBodyContent);
				break;
			case '#profile':
				window.profile.handleHash(injectBodyContent);
				break;
			case '#register':
				window.register.handleHash(injectBodyContent);
				break;
			case '#currenttrip':
				window.currenttrip.handleHash(injectBodyContent);
				break
			case '#previoustrips':
				window.previoustrips.handleHash(injectBodyContent);
				break;
			case '#qr_scanner':
				window.qr_scanner.handleHash(injectBodyContent);
				break;
			default: 
				break;
		}
	}

	function injectBodyContent(bodyContentHTML, afterInjectionCB){
		$bodyContent.html(bodyContentHTML);
		afterInjectionCB();
	}

	function getInitData(){
		if(window.localStorage.getItem('isLoggedIn'))
		{
		var obj=JSON.parse(window.localStorage.getItem('isLoggedIn'));
		$liUser.addClass('hidden');
		$liLogout.addClass('hidden');
		$liLogin.addClass('hidden');

			$liUser.find('a[info=user]').html('Hi ' + obj.FirstName);
			$liUser.removeClass('hidden');
			$liLogout.removeClass('hidden');
			//$liLogin.removeClass('hidden');
		}
		else{
			$.ajax({
			url: '/init',
			method: 'GET',
			data: {
			},
			success: getInitDataSH
		})
		}
			}

	function getInitDataSH(data){
		$liUser.addClass('hidden');
		$liLogout.addClass('hidden');
		$liLogin.addClass('hidden');
		if(data.IsAuthenticated){
			var obj={};	
			user = data.user
			userData = JSON.parse(user)
			$liUser.find('a[info=user]').html('Hi ' + userData.first_name);
			$liUser.removeClass('hidden');
			$liLogout.removeClass('hidden');
			obj.isLoggedIn=true;
			obj.FirstName=userData.first_name;
			obj.UserID=userData.UserId;
		window.localStorage.setItem('isLoggedIn',JSON.stringify(obj));
		} else {
			$liLogin.removeClass('hidden');
		}
		
	}

	// init
	function init(){
		window.trips.init();
		window.home.init();
		window.register.init();
		window.userhome.init();
		window.trips.init();
		window.login.init();
		window.qr_scanner.init();
		window.logout.init();
		window.currenttrip.init();
		window.profile.init();
		$(window).on('hashchange', handleHashChange);		
		handleHashChange();
		getInitData();
		window.location = '#home'
	}

	// init call
	init();
})();