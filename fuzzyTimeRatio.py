import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def member_of_function(crisp_value):
    # antecedent
    ratio = ctrl.Antecedent(np.arange(0, 2.1, 0.1), 'ratio')

    abcd = [[0, 0, 0.5, 1],
            [0.5, 0.75, 1.25, 1.5],
            [1, 1.5, 2, 2]]

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    ratio['comfortable'] = fuzz.trapmf(ratio.universe, abcd[0])
    ratio['hasty'] = fuzz.trapmf(ratio.universe, abcd[1])
    ratio['impossible'] = fuzz.trapmf(ratio.universe, abcd[2])     
    
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
    print member_of_function(0.6)