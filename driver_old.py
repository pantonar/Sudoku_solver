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
################################################################################
#               DEFINE WORKING DIRECTORY                                       # 
################################################################################
directory = r'/Users/pablo/Desktop/edx/artificial_intelligence/week8_sudoku/sudoku_solver'
#directory = r'C:\Users\Spare 3\Sudoku_solver'
os.chdir(directory)

################################################################################
#               IMPORT LIST OF SUDOKUS TO SOLVE                                # 
################################################################################
sudoku_start_file       = open('data/sudokus_start.txt')
sudoku_start            = sudoku_start_file.readlines()

sudoku_solutions        = open('data/sudokus_finish.txt').readlines()
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
        self.solved_board       = self.assign_start_board(string)
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
    Needs to be fed a sudoku_board instance to create the csp instance  

    Builds the CSP problem derived from the sudoku. A CSP consists of 3 attributes:
        1/ variable set
        2/ domain for each variable
        3/ all binary constraints (here pairwise variables that must be different)
    """
    
    def __init__(self,sudoku):
        self.variables          = list(sudoku.board.keys())
        self.domain             = self.get_domain(sudoku)
        self.neighbours         = self.get_neighbours()
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
        
    def solved(self):
        """ Returns True if the current domain for each variabel is unique (i.e. potential solution"""
        return not any(len(csp.domain[key])>1 for key in csp.domain)
    
csp = csp_sudoku(sudoku)
csp.variables
csp.domain
csp.neighbours
csp.constraints

################################################################################
#               ARC CONSISTENCY ALGORITHM                                      # 
################################################################################     
def AC3(csp):
    """
    Implements an Arc Consistency algorithm on a CSP problem: returns True if
    the CSP problem provided is arc-consistent, False otherwise. If False, the 
    problem cannot be solved
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
#               BACKTRACKING ALGORITHM                                         # 
################################################################################ 
def Backtracking_Search(csp):
    """Calls the backtrack algorithm"""
    return Backtrack({}, csp)

def Backtrack(assignment, csp):
    """ Backtracking algorithm:
        Takes an initial assignment of the solution, and the CSP problem
        csp object needs to have the following attributes:
            csp.neighbours
            csp.domain
            csp.variables
        assignment is a dictionary with keys the variable names
    """
    if complete(assignment, csp):
        return assignment
    
    variable = Select_Unassigned_Variable(assignment, csp)
    domain = deepcopy(csp.domain)
    print('New var selected: '+variable)
    print(Order_Domain_Value(variable, csp))
        
    for value in Order_Domain_Value(variable, csp):
        print(variable+': '+str(value))
        if consistent(variable, value, assignment, csp):
            print('Consistent')
            assignment.update({variable:value})
            inferences = {}
            inferences = Forward_Check(inferences, csp, variable, assignment, value)
            if inferences != False:
                print('Inferences made')
                #assignment.update(inferences)
                result = Backtrack(assignment, csp)
                if result!= False:
                    return result
            assignment.pop(variable)
            csp.domain.update(domain)
            print('Backtrack')
            print(len(assignment))
        print('Next value of '+variable)
    return False


def complete(assignment, csp):
    """ Checks assignment is complete, i.e. all variables in the CSP have been assigned """
    return set(assignment.keys()) == set(csp.variables)

def consistent(variable, value, assignment, cps):
    """ 
    Checks consistency, i.e. the value being assigned is not in conflict 
    with the CSP constraints (all neighbours have different values) 
    """
    for neighbour in set(csp.neighbours[variable]).intersection(set(assignment.keys())):
        if value == assignment[neighbour]:
            return False
    return True

def Select_Unassigned_Variable(assignment, csp):
    """ Implements MRV (Minimum Remaining Values) heuristic to choose which variable to assign next """
    potential_vars = {}
    for variable in csp.variables:
        if variable not in assignment.keys():
            potential_vars.update({variable : len(csp.domain[variable])})
    return min(potential_vars, key = potential_vars.get)

def Forward_Check(inferences, csp, variable, assignment, value):
    """ 
    Forward check that the assigned value will not yield any arc-inconsistency.
        1/ The domain of all neighbours is updated (i.e. value is removed).
        2/ If only one value left (i.e. a new value is found for assignemnt),
            then apply again the forward check on that variable
        3/ If in the process any variable's domain becomes empty, the initial 
            move is doomed to fail, and the function returns False
    """
    inferences[variable] = value
    
    for neighbour in csp.neighbours[variable]:
        if neighbour not in assignment:
            if value in csp.domain[neighbour]:
                if len(csp.domain[neighbour]) == 1:
                    return False       
                               
                csp.domain[neighbour].remove(value)
                values_left = deepcopy(csp.domain[neighbour])
                    
                if len(values_left) == 1:
                    next_layer = Forward_Check(inferences, csp, neighbour, assignment, values_left[0])
                    if next_layer == False:
                        return False
    return inferences
            
def Order_Domain_Value(variable, csp):
    """ No specific order in which to test variable assignments is chosen """
    return csp.domain[variable]

        
string = sudoku_start[10]
#string = list(solvable.keys())[1]
sudoku = sudoku_board(string)
csp = csp_sudoku(sudoku)
csp.domain
#AC3(csp)
csp.domain
a=Backtracking_Search(csp)
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
    #sudoku.print_board()
    csp = csp_sudoku(sudoku)
    if AC3(csp):
        count+=1
        if csp.solved():
            solvable.update({string : csp})
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
    
    
not any(len(solution.domain[key])>1 for key in solution.domain)
    
        
        
        


def test(csp):
    csp.domain['I9'] ='cuisi'
    return True



################################################################################
#               SOLVE ALL SUDOKUS WITH BTS                                     # 
################################################################################        
solvable  = {}

         
count = 0
for string in sudoku_start:
    sudoku = sudoku_board(string)
    csp = csp_sudoku(sudoku)
    a=Backtracking_Search(csp)
    if a != False:
        count += 1
        sudoku.solved_board.update(a)
        solvable.update({string : sudoku})
    else:
        print('The problem cannot be solved by BTS')
    
    
################################################################################
#               CHECK SOLUTIONS                                                # 
################################################################################  
    
def gen_string_sol(sudoku):
    sol =''
    for letter in sudoku.rows:
        for digit in sudoku.cols:
            sol+=str(sudoku.solved_board[letter+digit])
    return sol
    

solutions = []
for key in solvable.keys():
    sol = gen_string_sol(solvable[key])
    solutions.append(sol)

errors =0
for i in range(len(solutions)):
    if solutions[i] != sudoku_solutions[i][:-1]:
        errors+=1
        print('Error in solution')
     
            

    
    
    
    
    
    