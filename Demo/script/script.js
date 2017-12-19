const GRID = document.querySelector("#gridbody");
const CURTEMPVAL = document.querySelector("#curtempval");
const CURENERVAL = document.querySelector("#curenerval");

var boardSize = 8;
var numQueen = 8;
var numPawns = 2;
var showIntSteps = true;
var delay = 50;
var simRunning = false;

var board = [];
var emptyBoard = [];
var posQueens = [];

function buildGrid(n) {

	var shift = 1;
	clearGrid();

	for (let i = 0; i < n; i++) {	

		let newSpan = document.createElement("span");
		GRID.appendChild(newSpan);

		for (let j = 0; j < n; j++) {	

			let label = document.createElement("span");
			newSpan.appendChild(label);

			var position = (i * n) + j;

			if ((position + shift) % 2 == 0) {
				label.classList.add("labelType1");
			} else {
				label.classList.add("labelType2");
			}

			if (board[position] == 1) {
				placeQueen(label);
			}

			if (board[position] == 2) {
				label.classList.add("pawn");
			} 

			if (board[position] == 3) {
				label.classList.add("attack");
			} 
		}

		if (n % 2 == 0) {
			shift += 1;
		}
	}	
};

function placeQueen(label) {
	label.classList.add("queen");
}

function clearGrid() {
	GRID.innerHTML = "";
}

function genRandState(size, numq, nump = 2) {
	
	board = new Array(boardSize*boardSize).fill(0);

	var p = nump;
	while (p > 0) {
		
		let rand = Math.floor(Math.random() * size * size);
		if (board[rand] == 0) {
			board[rand] = 2;
			p--;
        }
	}

	emptyBoard = board.slice();

	var n = numq;
	positions = [];
	while (n > 0) {
		
		let rand = Math.floor(Math.random() * size * size);
		if (board[rand] == 0) {
			board[rand] = 1;
			positions.push(rand);			
			n--;
        }
	}

	buildGrid(size)
	return positions
}

function blockBoard(pos, board, n) {     

    //Go Left
    for (let i = 0; i < (pos % n); i++) {
    // for i in range(0, pos % n):
        if (board[pos - i - 1] == 0) {
            board[pos - i - 1] = 3;
        }
        else if (board[pos - i - 1] == 2){
            break;
        }
    }

    //Go Right
    for (let i = 0; i < ((n - 1) - (pos % n)); i++) {
    // for i in range(0, (n - 1) - (pos % n)):
        if (board[pos + i + 1] == 0) {
            board[pos + i + 1] = 3
        }
        else if (board[pos + i + 1] == 2){
            break
        }
    }

    //Go up  
    var up = pos - n
    while (up >= 0) {
        if (board[up] == 0) {
            board[up] = 3
        }
        else if (board[up] == 2){
            break
        }
        up -= n
    }
             
    //Go Down
    var dn = pos + n
    while (dn < n*n) {
        if (board[dn] == 0) {
            board[dn] = 3
        }
        else if (board[dn] == 2){
            break
        }
        dn += n
    }
     
    //Go Diagonally Left Up
    var dg = pos
    while ((dg % n) != 0 && dg > n) {
        dg -= (n + 1)
        if (board[dg] == 0) {
            board[dg] = 3
        }
        else if (board[dg] == 2) {
            break
        }
    }
              
    //Go Diagonally Right Down
    dg = pos
    while ((dg % n) != (n - 1) && dg < (n*n - n - 1)) {
        dg += (n + 1)
        if (board[dg] == 0){
            board[dg] = 3
        }
        else if (board[dg] == 2) {
            break
        }
    }
         
    //Go Diagonally Right Up
    dg = pos
    while ((dg % n) != (n - 1) && dg > (n - 1)) {
        if (board[dg - n + 1] == 0) {
            board[dg - n + 1] = 3
        }
        else if (board[dg - n + 1] == 2) {
            break
        }
        dg -= (n - 1)
    }

    //Go Diagonally Left Down
    dg = pos
    while ((dg % n) != 0 && dg < n * (n - 1)) {        
        if (board[dg + (n - 1)] == 0) {
            board[dg + (n - 1)] = 3
        }
        else if (board[dg + (n - 1)] == 2) {
            break
        }
        dg += (n - 1)
    }
}

function energyLevel(posLiz, s) {
     
    let l = posLiz.length;
    let energy = 0
     
    for (let i = 0; i < l; i++) {
        
        let tempBoard = emptyBoard.slice();
        // tempBoard.fill(0);
        blockBoard(posLiz[i], tempBoard, s)
        for (let j = i+1; j < l; j++) {
            if (tempBoard[posLiz[j]] == 3) {
                energy += 1
            }
        }
    }
    return energy

}

function printState(someBoard, size){

	for (let i = 0; i<size; i++) {
		str = " "
		for (let j = 0; j<size; j++) {
			str += someBoard[i * size + j];
		}
		console.log(str);
	}
}

function acceptState(delta, temp) {
    
    var pwr = delta/temp  
    prob = Math.exp(pwr)
    
    randProb =  Math.random()
    
    if (randProb < prob) {
        return true
    }
    
    return false
}

function nQueensSA (posQueens, showNewState) {

	let stateChanged = false;

	let tempState = board.slice();
	currentEnergy = energyLevel(posQueens, boardSize);
	// console.log("Current Energy: " + currentEnergy);

	while ( currentEnergy != 0 && currentTemp > 0 && x < 120 ) {

		currentTemp = 1 / Math.log(x);

		let randQueen = Math.floor(Math.random() * posQueens.length );
		let randPos = Math.floor(Math.random() * boardSize * boardSize);

		let newPosQueens = posQueens.slice();

		if (tempState[randPos] == 0) {

			newPosQueens[randQueen] = randPos;

			let newEnergy = energyLevel(newPosQueens, boardSize);

			if (newEnergy < currentEnergy) {
				tempState[randPos] = 1;
				tempState[posQueens[randQueen]] = 0;
				posQueens[randQueen] = randPos;
				currentEnergy = newEnergy;
				stateChanged = true;
			} else {
				if (acceptState((currentEnergy - newEnergy), currentTemp) == true) {
					tempState[randPos] = 1;
					tempState[posQueens[randQueen]] = 0;
					posQueens[randQueen] = randPos;
					currentEnergy = newEnergy
					stateChanged = true;
				}
			}
		} 

		x += 0.01
		if (showNewState == true && stateChanged == true) {
			break;
		}				
	}

	// console.log("New Energy: " + currentEnergy);
	board = tempState;
	buildGrid(boardSize);
	return posQueens;
}

function startSimulation(showNewState, speed = 100) {

	if (showNewState == false) {
		posQueens = nQueensSA(posQueens, showNewState);
		CURENERVAL.innerText = currentEnergy.toString().slice(0,5);
		CURTEMPVAL.innerText = currentTemp.toString().slice(0,5);
	} else {

		intervalID = window.setInterval(function() {

			posQueens = nQueensSA(posQueens, showNewState);
			CURENERVAL.innerText = currentEnergy.toString().slice(0,5);
			CURTEMPVAL.innerText = currentTemp.toString().slice(0,5);
			// console.log("Current Temp: " + currentTemp);
			if (currentEnergy == 0 || x == 119) {
				clearInterval(intervalID);
			}
		}, speed);
	}
}

function stopSimulation() {
	clearInterval(intervalID);	
	intervalID = 0;
}

function resetOptions() {	
	stopSimulation();
	simRunning = false;
	intervalID = 0;
	currentTemp = 10.01;
	x = 1.1;

	posQueens = genRandState(boardSize, numQueen, numPawns);
	currentEnergy = energyLevel(posQueens, boardSize);

	CURENERVAL.innerText = currentEnergy;
	CURTEMPVAL.innerText = currentTemp;
}

var intervalID = 0;
var currentTemp = 10.01;
var x = 1.1;

posQueens = genRandState(boardSize, numQueen);
var currentEnergy = energyLevel(posQueens, boardSize);

CURENERVAL.innerText = currentEnergy;
CURTEMPVAL.innerText = currentTemp;
// console.log("Current Energy: " + currentEnergy);






