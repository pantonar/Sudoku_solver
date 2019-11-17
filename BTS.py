#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:19:26 2019

@author: pablo

This script defines a a series of functions necessary to implement Backtracking-Search algorithm on a CSP problem
"""
from copy import deepcopy

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

    for value in Order_Domain_Value(variable, csp):
        if consistent(variable, value, assignment, csp):
            assignment.update({variable: value})
            inferences = {}
            inferences = Forward_Check(inferences, csp, variable, assignment, value)
            if inferences != False:
                result = Backtrack(assignment, csp)
                if result != False:
                    return result
            assignment.pop(variable)
            csp.domain.update(domain)
    return False


def complete(assignment, csp):
    """ Checks assignment is complete, i.e. all variables in the CSP have been assigned """
    return set(assignment.keys()) == set(csp.variables)


def consistent(variable, value, assignment, csp):
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
            potential_vars.update({variable: len(csp.domain[variable])})
    return min(potential_vars, key=potential_vars.get)


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
