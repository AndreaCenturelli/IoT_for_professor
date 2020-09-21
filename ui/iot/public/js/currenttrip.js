window.currenttrip = (function(){
	// var
    var parentClosure = {};
    var windowHR = {};
    var clients = [];

	// var init
	
	// functions
	function handleHash(htmlInjector){
        prepareHTML.htmlInjector = htmlInjector;
        
        $.ajax({
			url: '/startTrip',
			method: 'GET',
			data: {},
			success: startTripSH,
			error: function(){
				console.log(arguments);
			}
		});

		if(!prepareHTML.templateFunction){
			$.ajax({
				url: '/currenttrip-template',
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

	function startTripSH(data){
        if(data===false){
            window.alert("Error");
            window.location = "#userhome";
        }else{
            var userData = data.user;
            user = JSON.parse(userData);
            calculateWindow(user.Age,user.goal)
            mqqtData = JSON.parse(data.mqqtPoints);
            endpoints = mqqtData.endPoints;
            endpoints.forEach(endpoint => {
                broker = endpoint.broker;
                port = endpoint.port;
                topic = endpoint.topic;
                startConnect(broker,port,topic);
            });
        }
		
    }
    
    function endTrip(){
        $.ajax({
			url: '/endTrip',
			method: 'GET',
			dataType: 'text',
			data: {},
			success: endTripSH,
			error: function(){
				console.log(arguments);
			}
        });
        
		
    }
    
    function endTripSH(){

        startDisconnect();
        window.location = "#userhome";
    }

    // Called after form input is processed
    function startConnect(broker, port, topic) {
    
    // Generate a random client ID
    clientID = "clientID-" + parseInt(Math.random() * 100);

    // Initialize new Paho client connection
    client = new Paho.MQTT.Client("test.mosquitto.org", 8080, path='', clientID);
    clients.push(client);

    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // Connect the client, if successful, call onConnect function
    client.connect({ 
        onSuccess: onConnect,
    });
    }

    // Called when the client connects
    function onConnect() {
    // Subscribe to the requested topic
    client.subscribe(topic);
    }

    // Called when the client loses its connection
    function onConnectionLost(responseObject) {
        window.alert("connection lost... ERROR: " + responseObject.errorMessage);
    
    }

    // Called when a message arrives
    function onMessageArrived(message) {
    data = JSON.parse(message.payloadString);
    if(data.type === "speed"){
        value = data.value;
        unit = data.unit;
        parentClosure.divSpeed.innerHTML = '<span>' + value + ' ' + unit + '</span>';

    }else if(data.type === "heart_beat"){
        value = data.value;
        if(value < windowHR.min_window){
            parentClosure.divUp.removeClass('hidden');
            parentClosure.divDown.addClass('hidden');
        }else if(value > windowHR.max_window){
            parentClosure.divUp.addClass('hidden');
            parentClosure.divDown.removeClass('hidden');
        }else{
            parentClosure.divUp.addClass('hidden');
            parentClosure.divDown.addClass('hidden');
        }
        parentClosure.divHeartRate.innerHTML = '<span>' + value + ' BPM</span>';
    }
    
    }

    // Called when the disconnection button is pressed
    function startDisconnect() {
        clients.forEach(client => {
            client.disconnect();
        })
    }

    function calculateWindow(age, goal){
        var maxHR=220-Number(age);
        if (goal=="A"){
            windowHR.min_window=maxHR*0.5;
            windowHR.max_window=maxHR*0.6;
        }else if(goal=="B"){
            windowHR.min_window=maxHR*0.6;
            windowHR.max_window=maxHR*0.7;
        }else if(goal=="C"){
            windowHR.min_window=maxHR*0.7;
            windowHR.max_window=maxHR*0.8;
        }else if(goal=="D"){
            windowHR.min_window=maxHR*0.8;
            windowHR.max_window=maxHR*0.9;
        }else if(goal=="E"){
            windowHR.min_window=maxHR*0.9;
            windowHR.max_window=maxHR;
        }

    }

	
	function pageSetup(){
		// variables init
        parentClosure.btnEndTrip = $('#divCurrentTripTemplate #btnEndTrip');
        parentClosure.divSpeed = $('#divCurrentTripTemplate #divSpeed');
        parentClosure.divHeartRate = $('#divCurrentTripTemplate #divHeartRate');
        parentClosure.divUp = $('#divCurrentTripTemplate #divUp');
        parentClosure.divDown = $('#divCurrentTripTemplate #divDown');
		
		// events init
        parentClosure.btnEndTrip.on('click', endTrip);
        
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