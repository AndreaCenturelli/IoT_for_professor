module.exports = (function(){
	// var
	var path  = require('path');
    var pc = {};
	var request = require('request');
    const QRReader = require('qrcode-reader');
    const fs = require('fs');
    const jimp = require('jimp');

	// initialisation of variables

	// decalre functions
	function handleQRScannerTemplate(req, res){
		res.sendFile(
			path.join(
				__dirname, 
				'..\\templates', 
				'qr_scanner.hbs'));
    }
    
    async function handleQRScanner(req, res){
        const img = await jimp.read(fs.readFileSync('routes/qr_code.png'));

        const qr = new QRReader();
        
        var bikeId = ""
        var data ={}
        // qrcode-reader's API doesn't support promises, so wrap it
        const value = await new Promise((resolve, reject) => {
          qr.callback = (err, v) => err != null ? reject(err) : resolve(v);
          qr.decode(img.bitmap);
        }).catch(error => console.error(error.stack));
      
        
		bikeId = value.result;
		console.log(bikeId);
        userId = JSON.parse(req.userSession.user).id;

        data = {
            bikeId : bikeId,
            userId : userId
        }

        request.post({
			headers: {'content-type' : 'application/json'},
			url:     'http://127.0.0.1:8080/setbikedetails',
			body:    JSON.stringify(data)
		  }, function(error, response, body){
			if (error) {
				console.error(error)
				res.send(false)
			  }
			  console.log(`statusCode: ${response.statusCode}`)
			  console.log(body)
			  if(body != null && body != ''){

				req.userSession.bikeId = bikeId;
				
				res.send(req.userSession);
				}
				else {
					res.send(false);
				}
		  });
		
	}


	// declare init
	function init(routeConfig){
        routeConfig.app.get('/qr_scanner-template', handleQRScannerTemplate);
        routeConfig.app.post('/qr_scanner', handleQRScanner);
	}

	// return
	return {
		init: init
	}
})();