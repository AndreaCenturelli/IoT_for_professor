window.profile = (function(){
	// var
	var parentClosure = {};
	
	// var init
	// functions
	function handleHash(htmlInjector){
		debugger;
		prepareHTML.htmlInjector = htmlInjector;

		$.ajax({
			url: '/profile',
			method: 'GET',
			data: {
				
			},
			success: getDataSH,
			error: function(){
				console.log(arguments);
			}
		});

		if(!prepareHTML.templateFunction){
			$.ajax({
				url: '/profile-template',
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

	function getDataSH(data){
			prepareHTML.data = JSON.parse(data);
			prepareHTML();
		
	}

	function prepareHTML(){
		if(prepareHTML.data && prepareHTML.templateFunction){
			var html = prepareHTML.templateFunction(prepareHTML.data);
			prepareHTML.htmlInjector(html, pageSetup);
		}
	}

	function saveProfile(){
		window.event.preventDefault();
		var firstname = parentClosure.txtFirstName.val();
		var lastname = parentClosure.txtLastName.val();
		var email = parentClosure.txtEmail.val();
		var age = parentClosure.txtAge.val();
		var weight = parentClosure.txtWeight.val();
		var goaltypecode = parentClosure.txtGoalTypeCode.val();
		var goal = "";
		var leveloffitness = parentClosure.txtlevelOfFitness.val();
		var usertelegramid = parentClosure.txtUserTelegramId.val();
		var friendtelegramid = parentClosure.txtFriendTelegramId.val();
		var prof={};

		if(goaltypecode==="A"){
			goal = "Recovery"

		}else if(goaltypecode==="B"){
			goal = "Endurance Train"
		}else if(goaltypecode==="C"){
			goal = "Aerobic Capacity"
		}else if(goaltypecode==="D"){
			goal = "Lactate Threshold"
		}else if(goaltypecode==="E"){
			goal = "VO2"
		}
			
		prof.first_name=firstname;
		prof.last_name=lastname;
		prof.email=email;
		prof.age=age;
		prof.weight=weight;
		prof.goal=goal;
		prof.goaltypecode=goaltypecode;
		prof.leveloffitness=leveloffitness;
		prof.usertelegramid=usertelegramid;
		prof.friendtelegramid=friendtelegramid;

		$.ajax({
		url: '/profile',
		method: 'POST',
		dataType: 'text',
		data: prof,
		success: saveProfileSH,
		error: function(){
			console.log(arguments);
		}
		});
		

	}

	function saveProfileSH(){
		window.alert("Saved Successfully");
		window.location='';
	}

	function cancelPro(){
		window.location='';
	}

	
	
	function pageSetup(){
		// variables init
		parentClosure.txtFirstName=$('#divProfileTemplate #txtFirstName');
		parentClosure.txtLastName=$('#divProfileTemplate #txtLastName');
		parentClosure.txtEmail=$('#divProfileTemplate #txtEmail');
		parentClosure.txtAge=$('#divProfileTemplate #txtAge');
		parentClosure.txtWeight=$('#divProfileTemplate #txtWeight');
		parentClosure.txtGoalTypeCode=$('#divProfileTemplate #txtGoal');
		parentClosure.txtGoal=$('#divProfileTemplate #txtGoal option:selected');
		parentClosure.txtlevelOfFitness=$('#divProfileTemplate #txtlevelOfFitness');
		parentClosure.txtUserTelegramId=$('#divProfileTemplate #txtUserTelegramId');
		parentClosure.txtFriendTelegramId=$('#divProfileTemplate #txtFriendTelegramId');
		parentClosure.btnSave=$('#divProfileTemplate #btnSave');
		parentClosure.btnCancel=$('#divProfileTemplate #btnCancel');

		
		
		// events init
		parentClosure.btnSave.bind('click', saveProfile);
		parentClosure.btnCancel.bind('click', cancelPro);
		
		
		
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