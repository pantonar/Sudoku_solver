#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 13:16:23 2019

@author: pablo

Tests all the sudokus in sudoku_start can be solved by either AC3 or BTS

"""
from sudoku import *
from AC3 import *
from BTS import *
import sys

sudoku_start         = open('data/sudokus_start.txt').readlines()
sudoku_solutions     = open('data/sudokus_finish.txt').readlines()
f                    = open('test.txt', "w")

count = 0
for string_sudoku in sudoku_start:
    sudoku = sudoku_board(string_sudoku)
    csp = csp_sudoku(sudoku)
    # Check arc-consistency
    AC3(csp)
    if csp.solved():
        list_to_int(csp)
        sudoku.solved_board.update(csp.domain)
        if gen_string_sol(sudoku) == sudoku_solutions[count][:-1]:
            outcome = ' Correct'
        else:
            outcome = ' Incorrect'
        f.write(gen_string_sol(sudoku) + ' AC3' + outcome + ' \n')
    else:
        assignment = Backtracking_Search(csp)
        sudoku.solved_board.update(assignment)
        if gen_string_sol(sudoku) == sudoku_solutions[count][:-1]:
            outcome = ' Correct'
        else:
            outcome = ' Incorrect'

        f.write(gen_string_sol(sudoku) + ' BTS' + outcome + ' \n')
    count += 1
f.close()
