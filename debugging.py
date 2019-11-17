#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:19:26 2019

@author: pablo

SUDOKU SOLVER
run this program from the terminal using 'python driver.py <string_sudoku>'
to solve the sudoku

"""
import os
from copy import deepcopy
import sys
import time
import AC3
import BTS
import sudoku

################################################################################
#               DEFINE WORKING DIRECTORY                                       #
################################################################################
directory = r'/Users/pablo/Desktop/edx/artificial_intelligence/week8_sudoku/sudoku_solver'
# directory = r'C:\Users\Spare 3\Sudoku_solver'
os.chdir(directory)

################################################################################
#               IMPORT LIST OF SUDOKUS TO SOLVE                                #
################################################################################
sudoku_start_file = open('data/sudokus_start.txt')
sudoku_start = sudoku_start_file.readlines()

sudoku_solutions = open('data/sudokus_finish.txt').readlines()


################################################################################
#               DEBUGGING                                                       #
################################################################################

string = sudoku_start[10]
# string = list(solvable.keys())[1]
sudoku = sudoku_board(string)
csp = csp_sudoku(sudoku)
csp.domain
# AC3(csp)
csp.domain
a = Backtracking_Search(csp)
sudoku.solved_board.update(a)
sudoku.print_board('board')
print()
sudoku.print_board('solved_board')

solution = solvable[string]
sudoku = sudoku_board(string)
sudoku.print_board('board')
sudoku_solved = deepcopy(sudoku)
sudoku_solved.board.update(a)
print()
sudoku_solved.print_board()
################################################################################
#               SOLVE ALL SUDOKUS WITH AC3                                     #
################################################################################
solvable = {}
count = 0
for string in sudoku_start:
    sudoku = sudoku_board(string)
    # sudoku.print_board()
    csp = csp_sudoku(sudoku)
    if AC3(csp):
        count += 1
        if csp.solved():
            solvable.update({string: csp})
    else:
        if any(csp.domain[key] == [] for key in csp.domain):
            print('The problem cannot be solved as it is not arc-consistent')
    csp.domain

string = list(solvable.keys())[1]
solution = solvable[string]
sudoku = sudoku_board(string)
sudoku.print_board()
sudoku_solved = sudoku
sudoku_solved.board = solution.domain
print()
sudoku_solved.print_board()

not any(len(solution.domain[key]) > 1 for key in solution.domain)



################################################################################
#               SOLVE ALL SUDOKUS WITH BTS                                     #
################################################################################
solvable = {}

count = 0
for string in sudoku_start:
    sudoku = sudoku_board(string)
    csp = csp_sudoku(sudoku)
    a = Backtracking_Search(csp)
    if a != False:
        count += 1
        sudoku.solved_board.update(a)
        solvable.update({string: sudoku})
    else:
        print('The problem cannot be solved by BTS')


################################################################################
#               CHECK SOLUTIONS                                                #
################################################################################

def gen_string_sol(sudoku):
    sol = ''
    for letter in sudoku.rows:
        for digit in sudoku.cols:
            sol += str(sudoku.solved_board[letter + digit])
    return sol


solutions = []
for key in solvable.keys():
    sol = gen_string_sol(solvable[key])
    solutions.append(sol)

errors = 0
for i in range(len(solutions)):
    if solutions[i] != sudoku_solutions[i][:-1]:
        errors += 1
        print('Error in solution')








