window.register = (function(){
	// var
	var parentClosure = {};
	
	// var init
	// functions
	function handleHash(htmlInjector){
		debugger;
		prepareHTML.htmlInjector = htmlInjector;

		if(!prepareHTML.templateFunction){
			$.ajax({
				url: '/register-template',
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

	function register(){
		window.event.preventDefault();
		var firstname = parentClosure.txtFirstName.val();
		var lastname = parentClosure.txtLastName.val();
		var email = parentClosure.txtEmail.val();
		var age = parentClosure.txtAge.val();
		var weight = parentClosure.txtWeight.val();
		var goaltypecode = parentClosure.txtGoalTypeCode.val();
		var goal ="";
		var leveloffitness = parentClosure.txtlevelOfFitness.val();
		var usertelegramid = parentClosure.txtUserTelegramId.val();
        var friendtelegramid = parentClosure.txtFriendTelegramId.val();
        var password = parentClosure.txtPassword.val();
        var gender = parentClosure.txtGender.val();
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
        prof.password = password;
		prof.email=email;
        prof.age=age;
        prof.gender=gender;
		prof.weight=weight;
        prof.goal=goal;
        prof.goal_typecode=goaltypecode;
		prof.leveloffitness=leveloffitness;
		prof.usertelegramid=usertelegramid;
		prof.friendtelegramid=friendtelegramid;
		
		$.ajax({
		url: '/register',
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
		window.alert("Registered Successfully");
		window.location='#qr_scanner';
	}

	function cancelPro(){
		window.location='#home';
		window.location='';
	}

	
	
	function pageSetup(){
		// variables init
		parentClosure.txtFirstName=$('#divRegisterTemplate #txtFirstName');
		parentClosure.txtLastName=$('#divRegisterTemplate #txtLastName');
		parentClosure.txtEmail=$('#divRegisterTemplate #txtEmail');
		parentClosure.txtAge=$('#divRegisterTemplate #txtAge');
        parentClosure.txtWeight=$('#divRegisterTemplate #txtWeight');
        parentClosure.txtGender=$('#divRegisterTemplate #txtGender');
		parentClosure.txtGoalTypeCode=$('#divRegisterTemplate #txtGoal');
		parentClosure.txtlevelOfFitness=$('#divRegisterTemplate #txtlevelOfFitness');
		parentClosure.txtUserTelegramId=$('#divRegisterTemplate #txtUserTelegramId');
        parentClosure.txtFriendTelegramId=$('#divRegisterTemplate #txtFriendTelegramId');
        parentClosure.txtPassword=$('#divRegisterTemplate #txtPassword');
		parentClosure.btnSave=$('#divRegisterTemplate #btnSave');
		parentClosure.btnCancel=$('#divRegisterTemplate #btnCancel');

		
		
		// events init
		parentClosure.btnSave.bind('click', register);
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