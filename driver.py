#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:19:26 2019

@author: pablo

SUDOKU SOLVER
run this program from the terminal using 'python driver.py <string_sudoku>'
to solve the sudoku in <string_sudoku>

"""
from sudoku import *
from AC3 import *
from BTS import *
import sys


def main():
    string_sudoku       = sys.argv[1]
    sudoku              = sudoku_board(string_sudoku)
    csp                 = csp_sudoku(sudoku)
    f                   = open('output.txt', "w")
    # Check arc-consistency
    AC3(csp)
    if csp.solved():
        sudoku.solved_board.update
        f.write(gen_string_sol(sudoku)+' AC3'+'\n')
    else:
        assignment = Backtracking_Search(csp)
        sudoku.solved_board.update(assignment)
        f.write(gen_string_sol(sudoku)+' BTS'+'\n')
    f.close()


if __name__ == '__main__':
    main()