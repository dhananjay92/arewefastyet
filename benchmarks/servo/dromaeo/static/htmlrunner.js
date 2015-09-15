var startTest = startTest || function(){};
var test = test || function(name, fn){ fn(); };
var endTest = endTest || function(){};
var prep = prep || function(fn){ fn(); };


(function() {
	var testName = "";
	var testVersion = "";
	var startTime = 0;
	var endTime = 0;
	
	this.startTest = function(name, version){
		testName = name;
		testVersion = version;
		// Record the start time
		startTime = (new Date()).getTime();
	};
	this.endTest = function(name, version){
		// Record the end time
		endTime = (new Date()).getTime();
		
		var timeTaken = endTime - startTime;
		var results_json = {
			name: testName,
			version: testVersion,
			time: timeTaken
		};

		sendResults(results_json);

		// Automatically close the browser instance after 200 ms
		setTimeout(window.close(), 200);
	};

	sendResults = function(results) {
		var results = JSON.stringify(results);
		xmlhttp = new XMLHttpRequest();
		xmlhttp.open("POST", "/store_results");
		xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		xmlhttp.send(results);
	};
})();