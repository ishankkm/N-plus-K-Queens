# [N-plus-K-Queens](https://n-plus-k-queens.herokuapp.com/)

The problem is similar to the N-Queens problem, with an added complexity of having pawns on the board. 
As before, each pair of queens in the same row, column, or diagonal can attack each other.
The pawns block the queens from attacking each other if they lie between two attacking queens. 
However, they themselves do not attack any other piece. 

In this repository, there are four solutions to the problem each using a different search technique.
* Depth First Search using Recursion
* Depth First Search Iterative
* Breadth First Search
* Simulated Annealing

There are couple of automated testing codes which were used to test the correctness of the solutions.
These were also used for temperature tuning in Simulated Annealing method.

The repository also includes sample test cases.

### Check out a demo app for simulated annealing [here](https://n-plus-k-queens.herokuapp.com/)
