// sre.js
// A part of NonVisual Desktop Access (NVDA)
// This file is covered by the GNU General Public License.
// See the file COPYING for more details.
// Copyright (C) 2016 NV Access Limited

// Node.js script to bridge calls between NVDA and Speech Rule Engine

var sre = require("speech-rule-engine");
sre.setupEngine({semantics: true, domain: "mathspeak", style: "clearspeak"});

// Read and execute lines of code from stdin,
// pushing return information to stdout.
var readline = require("readline");
var rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout,
	terminal: false
});
rl.on("line", function(line){
	// Each line is a JSON-encoded string to eval.
	var code = JSON.parse(line);
	try{
		var ret = "ret " + JSON.stringify(eval(code));
	} catch (exc) {
		var ret = "exc " + exc;
	}
	console.log(ret);
})
