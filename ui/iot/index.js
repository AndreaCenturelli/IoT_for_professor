// requires
var express = require('express');
var bp = require('body-parser');
var session = require('./middleware/session');
var authentication = require('./middleware/authentication');
var authorisation = require('./middleware/authorisation');
var cp = require('cookie-parser');
var mainRoute = require('./routes/main');
var cors = require('cors');

// create app
var app = express();

// use it before all route definitions
app.use(cors());

// set middleware
app.use(express.static('public'));
app.use(bp.urlencoded({
  extended: true
}));
app.use(bp.json());
app.use(cp());
app.use(session);
app.use(authentication([]));
app.use(authorisation([]));




// set routes
mainRoute.init({
	app: app,
});

// respond with "hello world" when a GET request is made to the homepage
app.get('/test', function (req, res) {
  res.send('hello world')
})

// start application
app.listen(3000, function () {
  setInterval(function(){
  	var gs = global.sessions;

  	if(gs){
  		var prop;
  		for(prop in gs){
  			if(Date.now() - gs[prop].lastAccessedOn > 10 * 60 * 1000){
  				delete gs[prop];
  			}
  		}
  	}

  }, 1 * 60 * 60 * 1000);
  console.log('Example app listening on port 3000!');
});

