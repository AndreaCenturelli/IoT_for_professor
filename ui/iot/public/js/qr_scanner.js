window.qr_scanner = (function(){
	// var
	var parentClosure = {};
	var $liUser, $liLogout, $liLogin;


	// var init
	$liUser = $('#liUser');
	$liLogout = $('#liLogout');
	$liLogin = $('#liLogin');
	
	// functions
	function handleHash(htmlInjector){
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
		prepareHTML.htmlInjector = htmlInjector;

		if(!prepareHTML.templateFunction){
			$.ajax({
				url: '/qr_scanner-template',
				method: 'GET',
				dataType: 'text',
				data: {
				},
				success: getTemplateSH,
				error: function(){
					console.log(arguments);
				}
			});
		} 
	}

	function getTemplateSH(templateText){
		prepareHTML.templateFunction = Handlebars.compile(templateText);
		prepareHTML();
	}

	function prepareHTML(){
		if(prepareHTML.templateFunction && window.localStorage.getItem('isLoggedIn')){
			var html = prepareHTML.templateFunction({});
			prepareHTML.htmlInjector(html, pageSetup);
		}
	}

	function scanQR(){
        var data ={}
		$.ajax({
			url: '/qr_scanner',
			method: 'POST',
			dataType: 'text',
			data: {},
			success: qrSH,
			error: function(){
				console.log(arguments);
			}
		});
    }
    
    function qrSH(data){
        if(data==="false"){
			window.alert("Something wrong happend");
			window.location='#qr_scanner';

		}
		else{
			window.localStorage.setItem('bikeId',JSON.stringify({bikeId : data.bikeId}));
			console.log(data)
			window.location = '#userhome';
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
		prepareHTML();
	}

	function pageSetup(){
		// variables init
        parentClosure.btnQR = $('#divQrScannerTemplate #btnQR');
		
		// events init
        parentClosure.btnQR.on('click', scanQR);
        
	}

	// init
	function init(){
	}

	// return
	return {
		init: init,
		handleHash: handleHash
	}
})();