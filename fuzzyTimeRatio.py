import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def member_of_function(crisp_value):
    # antecedent
    ratio = ctrl.Antecedent(np.arange(0, 2.1, 0.1), 'ratio')

    means = [0,1.5,2]
    sigmas = [0.75,0.35,0.75]

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API
    ratio['comfortable'] = fuzz.gaussmf(ratio.universe, 0,1.5)
    ratio['hasty'] = fuzz.gaussmf(ratio.universe, 1.4,0.35)
    ratio['impossible'] = fuzz.gaussmf(ratio.universe, 2,0.75)    
    
    ratio.view()
    
    degrees = []
    keys = ratio.terms.keys()

    # computing membership degree for all linguistic variables
    for i, label in enumerate(keys):
        degrees.append(compute_degree(ratio, crisp_value, means[i], sigmas[i]))

    #returning linguistic variable for highest membership degree
    return keys[degrees.index(max(degrees))], degrees


def compute_degree(ratio, crisp_value, mean, sigma):
    # cast a higher ratio to 2 since that will always be impossible to make 
    if crisp_value > 2: 
        crisp_value = 2
    return fuzz.interp_membership(ratio.universe, fuzz.gaussmf(ratio.universe, mean, sigma), crisp_value)

if __name__ == '__main__':
    print member_of_function(1.0)