const butStartSim = document.querySelector("#butStartSim");
const butStopSim = document.querySelector("#butStopSim");
const inputNumQueen = document.querySelector("#numQueen");
const inputNumPawns = document.querySelector("#numPawns");
const simSpeed = document.querySelector("#simSpeed");
const reset = document.querySelector("#reset");

var timer = {
    running: false,
    iv: 5000,
    timeout: false,
    cb : function(){},
    start : function(cb,iv){
        var elm = this;
        clearInterval(this.timeout);
        this.running = true;
        if(cb) this.cb = cb;
        if(iv) this.iv = iv;
        this.timeout = setTimeout(function(){elm.execute(elm)}, this.iv);
    },
    execute : function(e){
        if(!e.running) return false;
        e.cb();
        e.start();
    },
    stop : function(){
        this.running = false;
    },
    set_interval : function(iv){
        clearInterval(this.timeout);
        this.start(false, iv);
    }
};

butStartSim.addEventListener("click", function() {
	simRunning = true;
	startSimulation(showIntSteps, delay);
}, false);

butStopSim.addEventListener("click", function() {
	simRunning = false;
	stopSimulation()
}, false);

inputNumQueen.addEventListener("change", function() {
	stopSimulation();
	let n = parseInt(inputNumQueen.value);
	numQueen = n;
	resetOptions();
});

inputNumPawns.addEventListener("change", function() {
	stopSimulation();
	let n = parseInt(inputNumPawns.value);
	numPawns = n;
	resetOptions();
});

showstep.addEventListener("change", function() {
	clearInterval(intervalID);	
	intervalID = 0;

	let val = showstep.checked;
	showIntSteps = val;
	
	if (simRunning == true) {
		startSimulation(showIntSteps, delay);
	} 
});

simSpeed.addEventListener("change", function() {
	
	clearInterval(intervalID);	
	intervalID = 0;

	let val = parseInt(simSpeed.value);
	val = 600 - val;
	delay = val;
	if (simRunning == true) {
		startSimulation(showIntSteps, delay);
	} 
});

reset.addEventListener("click", function() {
	simRunning = false;
	stopSimulation();
	resetOptions();
});

function changeBoardSize() {
	stopSimulation();
	var select = document.querySelector("#bszsel");
	boardSize = parseInt(select.value);
	resetOptions();
}