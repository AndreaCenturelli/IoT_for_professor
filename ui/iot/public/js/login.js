window.login = (function(){
	// var
	var parentClosure = {};

	// var init
	
	// functions
	function handleHash(htmlInjector){
		prepareHTML.htmlInjector = htmlInjector;

		if(!prepareHTML.templateFunction){
			$.ajax({
				url: '/login-template',
				method: 'GET',
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
		if(prepareHTML.templateFunction){
			var html = prepareHTML.templateFunction({});
			prepareHTML.htmlInjector(html, pageSetup);
		}
	}

	function login(){

		var email = parentClosure.txtUserId.val();
			var re=/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	    	if(!re.test(email)){
			window.alert("Enter valid Email Id");
			return;
			}
		var pwd = parentClosure.txtPassword.val();
		
		var data = {
			password: pwd,
			email: email
		}
		$.ajax({
			url: '/login',
			method: 'POST',
			dataType: 'text',
			data: data,
			success: loginSH,
			error: function(){
				console.log(arguments);
			}
		});
		//window.event.preventDefault();
	}

	function loginSH(data){
		if(data==="false"){
			window.alert("Enter the correct credentials");
			parentClosure.txtUserId.val('');
			parentClosure.txtPassword.val('');
			window.location='#login';

		}
		else{
		window.location = '#qr_scanner';
		console.log(data)
		}
	}

	function cancelPro(){
		window.location='#home';
	}

	function pageSetup(){
		// variables init
		parentClosure.txtUserId = $('#divLoginTemplate #txtUserId');
		parentClosure.txtPassword = $('#divLoginTemplate #txtPassword');
		parentClosure.btnLogin = $('#divLoginTemplate #btnLogin');
		parentClosure.btnCancel=$('#divRegisterTemplate #btnCancel');
		
		// events init
		parentClosure.btnLogin.on('click', login);
		parentClosure.btnCancel.on('click', cancelPro);
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