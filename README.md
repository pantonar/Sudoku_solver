# Sudoku_solver
Sudoku solver using backtracking and AC3 algotithm

AC3 function checks arc-consistency on all the CSP constraints, and reduces the domains accordingly

Backtracking implementation uses the following heuristics:
  1/ Minimum Remaning Values: next variable to assign a value to is the one with the smallest domain
  2/ Forward check using arc-consistency: each assignment is checked against being arc-consistent. If not, backtrack.
  
  
 driver.py can be called from command line with a string of 81 characters, for the starting sudoku state
 
 Folder data:
 Contains 400 starting sudokus and their solution, that I used to test the implementation
