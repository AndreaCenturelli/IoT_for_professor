window.home = (function(){
	// var
	var parentClosure = {};

	// var init
	
	// functions
	function handleHash(htmlInjector){
		prepareHTML.htmlInjector = htmlInjector;

		if(!prepareHTML.templateFunction){
			$.ajax({
				url: '/home-template',
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

		window.location='#login';
	}

	function register(){

		window.location='#register';
		
	}

	function pageSetup(){
		// variables init
        parentClosure.btnLogin = $('#divHomeTemplate #btnLogin');
        parentClosure.btnRegister = $('#divHomeTemplate #btnRegister');
		
		// events init
        parentClosure.btnLogin.on('click', login);
        parentClosure.btnRegister.on('click', register);
        
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