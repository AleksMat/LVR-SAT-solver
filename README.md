# LVR-SAT-solver #
Project for course Logika v računalništvu
Fakulteta za matematiko in fiziko, Ljubljana
March 2016

### Authors ###

* Jure Kukovec
* Matej Aleksandrov

### About program ###

Program is used for solving arbitrary SAT problem quite efficiently. It uses DPLL algorithm with DFS searches over variables and clauses.

### How To Use ###

* Run program SAT.py
* Call function solve( ... ). As input of function you can write:
	* Name of file with Dimacs formula. E.g. **solve("fileName.txt")** or **solve("fileName.cnf")**
	* Index of a sample file listed in the program SAT.py. E.g. **solve(0)**, **solve(1)**,... 
* Alternatively, the program can be called from the command line with the file name or sample number as the first parameter
* The answer will be written in file "fileName_solution.txt". Program will also inform you about it's running time.
* Answer will be in requred form and numbers will be sorted by their absolute value. If formula won't have a solution, the answer will be *NOT SATISFIABLE*.

### Sample generation ###

In sample_gen, the generator.py file can be used to produce Dimacs formulas for the following SAT problem:
Given a n x n chess board with several black queens, where can the white king be placed, so that he is not in check?

To generate samples, the produceDIMACS function can be called with 3 arguments:
 * queens, a list of tuples specifzing queen positions
 * outFileName, the file name where the resulting formula is saved
 * boardDim, the board dimension
Alternatively, generateSample can be called with:
 * dim, the board dimension and number of queens
 * outName, the file name where the resulting formula is saved
which selects dim unique random positions to place the queens.

Note that the problem generated need not be satisfiable.


