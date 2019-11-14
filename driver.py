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

################################################################################
#               DEFINE WORKING DIRECTORY                                       # 
################################################################################
directory = r'/Users/pablo/Desktop/edx/artificial_intelligence/week8_sudoku'
directory = r'C:\Users\Spare 3\Sudoku_solver'
os.chdir(directory)

################################################################################
#               IMPORT LIST OF SUDOKUS TO SOLVE                                # 
################################################################################
sudoku_start_file       = open('data/sudokus_start.txt')
sudoku_start            = sudoku_start_file.readlines()

################################################################################
#               FUNCTIONS AND CLASSESS                                        # 
################################################################################
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
#        self.possible_values    = self.start_possible_values()
        
        
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
    
    def print_board(self):
        """
        Prints the board dict in the terminal, indicating where the small 
        squares are located
        """
        length = 0
        line        = str()
        delimiter   = str()
        for key in self.board.keys():              
            try:
                line += str(self.board[key][0])+' '
            except TypeError:
                line += str(self.board[key])+' '
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
                    
#    def start_possible_values(self):
#        d = {}
#        for letter in self.rows:
#            for digit in self.cols:
#                key = letter+digit
#                if self.board[key] != 0:
#                    d.update({key : self.board[key]})
#                else:
#                    self.column_domain
#                
        
string = sudoku_start[0]
sudoku = sudoku_board(string)
sudoku.print_board()
sudoku.board

    
    

class csp_sudoku:
    """
    Needs to be fed a sudoku_board instance to creat the csp instance  

    Builds the CSP problem derived from the sudoku. A CSP consists of 3 attributes:
        1/ variable set
        2/ domain for each variable
        3/ all binary constraints (here pairwise variables that must be different)
    """
    
    def __init__(self,sudoku):
        self.variables          = list(sudoku.board.keys())
        self.domain             = self.get_domain()
        self.neighbours         = self.get_neighbours()
        self.constraints        = self.gen_binary_constraints()
        
        
    def get_domain(self):
        """Returns a dictionary with the domain of each of the 81 variables"""
        domain = {}
        for variable in self.variables:
            if sudoku.board[variable] != 0:
                domain.update({variable:[sudoku.board[variable]]})
            else:
                domain.update({variable : [int(i) for i in sudoku.cols]})
        return domain
                
    def get_neighbours(self):
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
        
        
csp = csp_sudoku(sudoku)
csp.variables
csp.domain
csp.neighbours
csp.constraints

      
def AC3(csp):
    """
    Implements an Arc Consistency algorithm on a CSP problem.
    The CSP object has to be fed to the AC3 function, where:
            1/ csp.variables    : is a list with all the variable names to be 
                                  assigned to solve the CSP
            2/ csp.domain       : is a dictionary, whose keys are csp.variables,
                                  and gets the domain on which each variable value 
                                  has to come from
            3/ csp.constraints  : is a set of binary combinations of elements in 
                                  csp.variables that hold constraints. Constraints
                                  are assumed to be 'different than' (i.e. both
                                  elements in each binary combination have to be 
                                  different). Hence the argument is a binary CSP
            4/ csp.neighbours   : a dictionary where the key gives a set of its
                                  neighbours (variables that are related to it by
                                  a constraint)
    """
    queue = csp.constraints
    
    while bool(queue):
        pair        = queue.pop()
        Xi          = pair[0]
        domain_Xi   = csp.domain[Xi]
        Xj          = pair[1]
        domain_Xj   = csp.domain[Xj]
        
        if Revise(csp, Xi, Xj, domain_Xi, domain_Xj):
            if bool(domain_Xi):
                for x in (csp.neighbours[Xi] - {Xj}):
                    queue.update([(x, Xi)])
            else:
                return False
                   
    return True
                   
def Revise(csp, Xi, Xj, domain_Xi, domain_Xj):
    """ Returns True if the domain of Xi is revised """
    revise = False
    for x in domain_Xi:
        if not any(x!=y for y in domain_Xj):
            csp.domain[Xi].remove(x)
            revise = True
    return revise



################################################################################
#               SOLVE ALL SUDOKUS WITH AC3                                     # 
################################################################################        
solvable = {}         
for string in sudoku_start:
    sudoku = sudoku_board(string)
    #sudoku.print_board()
    csp = csp_sudoku(sudoku)
    if AC3(csp):
        if not any(len(csp.domain[key])>1 for key in csp.domain):
            solvable.update({string : csp})
    csp.domain
    
    
string = list(solvable.keys())[0]
solution = solvable[string]
sudoku = sudoku_board(string)
sudoku.print_board()
sudoku_solved = sudoku  
sudoku_solved.board = solution.domain
sudoku_solved.print_board()
    
    
not any(len(solution.domain[key])>1 for key in solution.domain)
    
        
        
        
    
    
    