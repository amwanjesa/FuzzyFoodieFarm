import matplotlib
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def member_of_function(crisp_value):
    # antecedent
    ratio = ctrl.Antecedent(np.arange(0, 2.1, 0.1), 'ratio')

    abcd = [[0, 0, 0.25, 0.5],
            [0.25, 0.5, 0.75, 1.25],
            [0.75, 1.25, 1.5, 1.75],
            [1.5, 1.75, 2, 2]]

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    ratio['ample time'] = fuzz.trapmf(ratio.universe, abcd[0])
    ratio['comfortable'] = fuzz.trapmf(ratio.universe, abcd[1])
    ratio['hasty'] = fuzz.trapmf(ratio.universe, abcd[2])
    ratio['impossible'] = fuzz.trapmf(ratio.universe, abcd[3])   
    
    degrees = []
    keys = ratio.terms.keys()

    # computing membership degree for all linguistic variables
    for i, label in enumerate(keys):
        degrees.append(compute_degree(ratio, crisp_value, abcd[i]))

    #returning linguistic variable for highest membership degree
    return keys[degrees.index(max(degrees))], degrees


def compute_degree(ratio, crisp_value, abcd):
    # cast a higher ratio to 2 since that will always be impossible to make 
    if crisp_value > 2: 
        crisp_value = 2
    return fuzz.interp_membership(ratio.universe, fuzz.trapmf(ratio.universe, abcd), crisp_value)

if __name__ == '__main__':
    print member_of_function(0.1)