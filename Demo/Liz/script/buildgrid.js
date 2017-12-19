function acceptState(delta, temp) {
    
    var pwr = delta/temp  
    prob = Math.exp(pwr)
    
    randProb =  Math.random()
    
    if (randProb < prob) {
        return True
    }
    
    return False
}