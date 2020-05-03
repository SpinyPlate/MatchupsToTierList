#!/usr/bin/env python

import numpy as np

def get_N(prob_table):
    # Assumes input is square
    return prob_table.shape[0]

def convert_match_ups_to_probabilities(match_ups):
    return match_ups/100

def sanity_check(prob_table):
    input_valid = True
    dims = prob_table.shape
    if(dims[0] != dims[1]):
        print('Dimensions must be equal!')
        return False
    N = dims[0]
    i = 0
    while i < N:
        j = i
        while j < N:
            if( (prob_table[i][j] + prob_table[j][i]) != 1):
                print(
                    'Probabilities do not sum to 1 for indices ' +
                    str(i) + ', ' +str(j) +
                    ', sum was ' + str(prob_table[i][j] + prob_table[j][i])
                )
                input_valid = False
            j += 1
        i += 1
    return input_valid

def normalise(vector):
    # Assumes input is 1D
    vector_sum = np.sum(vector)
    if vector_sum == 0:
        return vector
    return vector/vector_sum

def check_convergence(new_prevalences, prevalences, rtol = 0.00001):
    return np.allclose(new_prevalences, prevalences, rtol)

def main():
    # Assume input has no row or column headers
    # Just a N x N array of percentages (i.e. out of 100 not out of 1)
    # Number indicates probability of row character beating column character
    match_ups = np.genfromtxt('ssbm_matchups.csv', delimiter=' ')
    print('Input:')
    print(match_ups)
    prob_table = convert_match_ups_to_probabilities(match_ups)
    input_valid = sanity_check(prob_table)
    if not input_valid:
        return
    prevalences = np.full((get_N(prob_table), 1), 1/get_N(prob_table))
    win_chances = None
    converged = False
    while not converged:
        win_chances = prob_table.dot(prevalences)
        new_prevalences = normalise(win_chances)
        converged = check_convergence(new_prevalences, prevalences)
        prevalences = new_prevalences
    print()
    print('Output:')
    print('Win chances = ')
    print(win_chances)
    print('Prevalences = ')
    print(prevalences)

if __name__ == '__main__':
    main()
