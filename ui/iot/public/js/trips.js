window.trips = (function(){
	// var
	var parentClosure = {};

	// var init
	
	// functions
	function handleHash(htmlInjector){
        prepareHTML.htmlInjector = htmlInjector;
        
        $.ajax({
			url: '/previousTrips',
			method: 'GET',
			data: {},
			success: previousTripsSH,
			error: function(){
				console.log(arguments);
			}
		});

		if(!prepareHTML.templateFunction){
			$.ajax({
				url: '/trips-template',
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
		if(prepareHTML.data && prepareHTML.templateFunction){
			var html = prepareHTML.templateFunction(prepareHTML.data);
			prepareHTML.htmlInjector(html, pageSetup);
		}
	}

	function previousTripsSH(rxdata){
		if(rxdata.IsAuthenticated === false){
			var html = 'Please <a href="#login">Login</a> to access issues';
			prepareHTML.htmlInjector(html, null);
		}else{
			if(rxdata===false){
				window.alert("Error");
				window.location = "#userhome";
			}else{
				var tripsData = JSON.parse(rxdata);
				tripsData.trips.forEach(trip => {
					var date = new Date(trip.datetime + ' UTC');
					trip.datetime = date.toLocaleString();                 
				});
				prepareHTML.data = tripsData.trips;
				prepareHTML();
			}	
		}
	}

	function showDetails(){
		var tripId=$(this).closest('div[trip-id]').attr('trip-id');
		$.ajax({
			url: '/getTrip',
			method: 'POST',
			dataType: 'text',
			data: {
				tripId : tripId
			},
			success: showDetailsSH,
			error: function(){
				console.log(arguments);
			}
		});

	}

	function showDetailsSH(data){
		debugger;
		if(data===false){
			window.alert("Error");
		}else{
			tripData = JSON.parse(data);
			parentClosure.txtTripDate.val(new Date(tripData.datetime + ' UTC').toLocaleString());
			parentClosure.txtAverageSpeed.val(tripData.avg_speed + ' km/h');
			parentClosure.txtAverageHeartRate.val(tripData.avg_heart_rate + ' BPM');
			parentClosure.txtMaximumSpeed.val(tripData.max_speed + ' km/h');
			parentClosure.txtMaximumHeartRate.val(tripData.max_heart_rate + ' BPM');
			parentClosure.txtMinimumHeartRate.val(tripData.min_heart_rate + ' BPM');
			parentClosure.divSpeedPlot.innerHTML = '<img class="media-object img-fluid img-thumbnail" src="' + tripData.speed_plot + '" width="200" height="300">';
			parentClosure.divHeartRatePlot.innerHTML = '<img class="media-object img-fluid img-thumbnail" src="' + tripData.heart_rate_plot + '" width="200" height="300">';
			parentClosure.divMap.innerHTML = '<embed type="text/html" src="' + tripData.map + '" width="200" height="300">';
			parentClosure.tripModal.modal('show');
		}	
	}


	function pageSetup(){
        // variables init
		parentClosure.divTrips = $('#divTripsTemplate #divTrips');
		parentClosure.tripModal = $('#divTripsTemplate #tripModal');
		parentClosure.modalTitle1 = $('#divTripsTemplate #modalTitle1');
		parentClosure.txtTripDate = $('#divTripsTemplate #txtTripDate');
		parentClosure.txtAverageSpeed = $('#divTripsTemplate #txtAverageSpeed');
		parentClosure.txtAverageHeartRate = $('#divTripsTemplate #txtAverageHeartRate');
		parentClosure.txtMaximumSpeed=$('#divTripsTemplate #txtMaximumSpeed');
		parentClosure.txtMaximumHeartRate=$('#divTripsTemplate #txtMaximumHeartRate');
		parentClosure.txtMinimumHeartRate=$('#divTripsTemplate #txtMinimumHeartRate');
		parentClosure.divSpeedPlot=$('#divTripsTemplate #divSpeedPlot');
		parentClosure.divHeartRatePlot=$('#divTripsTemplate #divHeartRatePlot');
		parentClosure.divMap=$('#divTripsTemplate #divMap');
		parentClosure.divTrips.on('click', 
			'a[action=view]', showDetails);
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