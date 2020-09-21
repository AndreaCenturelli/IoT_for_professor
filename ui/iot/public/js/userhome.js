window.userhome = (function(){
	// var
	var parentClosure = {};

	// var init
	
	// functions
	function handleHash(htmlInjector){
		prepareHTML.htmlInjector = htmlInjector;

		if(!prepareHTML.templateFunction){
			$.ajax({
				url: '/userhome-template',
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

	function startTrip(){
		
		window.location = '#currenttrip';	
	}

	function previousTrips(){
		window.location = '#trips';
			
	}

	function pageSetup(){
		// variables init
        parentClosure.btnStartTrip = $('#divUserHomeTemplate #btnStartTrip');
        parentClosure.btnPreviousTrips = $('#divUserHomeTemplate #btnPreviousTrips');
		
		// events init
        parentClosure.btnStartTrip.on('click', startTrip);
        parentClosure.btnPreviousTrips.on('click', previousTrips);
        
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