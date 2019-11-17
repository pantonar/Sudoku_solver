#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:19:26 2019

@author: pablo

This script defines two classes:
    1/ sudoku_board     : from a string, creates a sudoku object that can print itself
    2/ csp_sudoku       : taking a sudoku object, instance of sudoku_board, transforms the problem to a CSP setup
"""

class sudoku_board:
    """
    Class representing the Sudoku game.
    Attributes:
        self.board  : dictionary where tiles A1 to I9 are the keys of the tile value
        self.rows   : row names, A to I
        self.cols   : column names, 1 to 9
    Method:
        self.print_board()  : prints the sudoku game in the terminal
    """

    def __init__(self,string):
        self.rows               = 'ABCDEFGHI'
        self.cols               = '123456789'
        self.board              = self.assign_start_board(string)
        self.solved_board       = self.assign_start_board(string)


    def assign_start_board (self, string):
        """
        Given the string og length 81, returns a dictionary where each board
        tile are assigned the corresponding starting value
        """
        d = {}
        index = 0
        for letter in self.rows:
            for digit in self.cols:
                d.update({letter+str(digit):int(string[index])})
                index += 1
        return d

    def print_board(self, board = 'board'):
        """
        Prints the board dict in the terminal, indicating where the small
        squares are located. Takes an argument:
            board   : either 'board' or 'solved_board'
        """
        length = 0
        line        = str()
        delimiter   = str()
        if board == 'board':
            board = self.board
        elif board == 'solved_board':
            board = self.solved_board
        else:
            KeyError('Enter valid argument')

        for key in board.keys():
            try:
                line += str(board[key][0])+' '
            except TypeError:
                line += str(board[key])+' '
            if key[1] in '36':
                line += '| '
            if  key[0] in 'CF':
                delimiter += '--'
                if  key[1] in '36':
                    delimiter += '+-'
            length +=1

            if length == 9:
                print(line)
                length      = 0
                line        = str()
                if len(delimiter)>0:
                    print(delimiter)
                    delimiter   = str()


class csp_sudoku:
    """
    Needs to be fed a sudoku_board instance to create the csp instance

    Builds the CSP problem derived from the sudoku. A CSP consists of 3 attributes:
        1/ variable set
        2/ domain for each variable
        3/ all binary constraints (here pairwise variables that must be different)
    """

    def __init__(self,sudoku):
        self.variables          = list(sudoku.board.keys())
        self.domain             = self.get_domain(sudoku)
        self.neighbours         = self.get_neighbours(sudoku)
        self.constraints        = self.gen_binary_constraints()


    def get_domain(self, sudoku):
        """Returns a dictionary with the domain of each of the 81 variables"""
        domain = {}
        for variable in self.variables:
            if sudoku.board[variable] != 0:
                domain.update({variable:[sudoku.board[variable]]})
            else:
                domain.update({variable : [int(i) for i in sudoku.cols]})
        return domain

    def get_neighbours(self, sudoku):
        """
        Returns a dictionary with a list of all the 'neighbours' of the key,
        that is all the tiles that must have a different value than the key
        """
        neighbours = {}
        for variable in self.variables:
            letter  = variable[0]
            digit   = variable[1]
            n       = (int(digit)-1)//3
            row     = (sudoku.rows.find(letter))//3
            square  = []

            for i in ['123','456','789'][n]:
                for j in ['ABC','DEF','GHI'][row]:
                    square.append(j+i)

            neighbours.update({variable: set([letter + i for i in sudoku.cols] +
                                             [i + digit for i in sudoku.rows] +
                                             square) - set([variable,variable])})
        return neighbours

    def gen_binary_constraints(self):
        """
        Get all the binary constraints between tiles: a set with all the pairs that must be distinct
        """
        return {(variable, neighbour) for variable in self.variables for neighbour in self.neighbours[variable]}

    def solved(self):
        """ Returns True if the current domain for each variabel is unique (i.e. potential solution"""
        return not any(len(self.domain[key])>1 for key in self.domain)

def gen_string_sol(sudoku):
    """Takes a sudoku object and returns a string with all the assignment in solved_board attribute"""
    sol =''
    for letter in sudoku.rows:
        for digit in sudoku.cols:
            sol+=str(sudoku.solved_board[letter+digit])
    return sol

def list_to_int(csp):
    for key in csp.domain:
        csp.domain[key] = csp.domain[key][0]
