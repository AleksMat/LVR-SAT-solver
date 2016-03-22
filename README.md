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
	* Name of file with Dimacs formula. 
	E.g. solve("fileName.txt") or solve("fileName.cnf")
	* Index of a sample file listed in the program SAT.py. 
	E.g. solve(0), solve(1),... 
* The answer will be written in file "fileName_solution.txt". Program will also inform you about it's running time.
