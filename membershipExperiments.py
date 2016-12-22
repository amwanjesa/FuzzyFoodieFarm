import numpy as np
import skfuzzy.control as ctrl
import skfuzzy as fuzz
import fuzzyTimeRatio as timefuzz


# We can simulate at higher resolution with full accuracy

y = []

array = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
# Loop through the system 21*21 times to collect the control surface
for i in array:
    ratio = ctrl.Antecedent(np.arange(0, 2.1, 0.1), 'ratio')
    
    abcd = [[0, 0, 0.5, 1],
            [0.5, 0.75, 1.25, 1.5],
            [1, 1.5, 2, 2]]

    # Custom membership functions can be built interactively with a familiar,
    # Pythonic API 
    ratio['comfortable'] = fuzz.gaussmf(ratio.universe, 0,1.5)
    ratio['hasty'] = fuzz.gaussmf(ratio.universe, 1.4,0.35)
    ratio['impossible'] = fuzz.gaussmf(ratio.universe, 2,0.75) 
   
    ratio_comfortable = fuzz.interp_membership(ratio.universe, fuzz.gaussmf(ratio.universe, 0,1.5),i)
    ratio_hasty = fuzz.interp_membership(ratio.universe, fuzz.gaussmf(ratio.universe, 1.4,0.35),i)
    ratio_impossible = fuzz.interp_membership(ratio.universe, fuzz.gaussmf(ratio.universe, 2,0.75),i)
        
    x_fit = np.arange(0, 1.1, 0.1)
    
    fit_terrible = fuzz.trapmf(x_fit, [0, 0, 0.25, 0.375])
    fit_bad = fuzz.trapmf(x_fit, [0.25, 0.375, 0.5, 0.675])
    fit_decent = fuzz.trapmf(x_fit, [0.5, 0.675, 0.75, 0.875])
    fit_good = fuzz.trapmf(x_fit, [0.75, 0.875, 1, 1])
    
    activation_rule1 = np.fmin(ratio_impossible, fit_terrible)
    activation_rule2 = np.fmin(ratio_hasty, np.fmax(fit_bad, fit_decent))
    activation_rule3 = np.fmin(ratio_comfortable, fit_good)
        
    # Aggregate all three output membership functions together
    aggregated = np.fmax(activation_rule1, np.fmax(activation_rule2, activation_rule3))
    output = fuzz.defuzz(x_fit, aggregated, 'bisector')
    y.append(output)

# Plot the result in pretty 3D with alpha blending
import matplotlib.pyplot as plt
plt.plot(array, y)
plt.title('bisector + trap ratio + gauss fit')
plt.show()