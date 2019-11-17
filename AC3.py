#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:19:26 2019

@author: pablo

This script defines a function checking arc-consistency of a CSP problem
"""
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

