import numpy as np
import skfuzzy as fuzz
import heapq

def defuzzify(ratio_degrees, u, activities, chosen):
    
    ratio_comfortable = ratio_degrees[0]
    ratio_hasty = ratio_degrees[1]
    ratio_impossible = ratio_degrees[2]
    
    activity_postworkout = u[0]
    activity_study = u[1]
    activity_life = u[2]
    activity_sport = u[3]
    
    x_fit = np.arange(0, 1.1, 0.1)
    
    fit_terrible = fuzz.trapmf(x_fit, [0, 0, 0.25, 0.375])
    fit_bad = fuzz.trapmf(x_fit, [0.25, 0.375, 0.5, 0.675])
    fit_decent = fuzz.trapmf(x_fit, [0.5, 0.675, 0.75, 0.875])
    fit_good = fuzz.trapmf(x_fit, [0.75, 0.875, 1, 1])
    
    
    indexChosen = activities.index(chosen)
    degreesActivities = [activity_postworkout, activity_study, activity_life, activity_sport]

    activation_rule1 = np.fmin(ratio_impossible, fit_terrible)

    sortedIndices = heapq.nlargest(4, xrange(len(degreesActivities)), key=degreesActivities.__getitem__)
    
    if sortedIndices[0] == indexChosen: 
        rule2 = np.fmin(ratio_hasty, degreesActivities[indexChosen])
        activation_rule2 = np.fmin(rule2, fit_decent)
        rule3 = np.fmin(ratio_comfortable, degreesActivities[indexChosen])
        activation_rule3 = np.fmin(rule3, fit_good)
    elif sortedIndices[1] == indexChosen: 
        rule2 = np.fmin(ratio_hasty, degreesActivities[indexChosen])
        activation_rule2 = np.fmin(rule2, fit_bad)
        rule3 = np.fmin(ratio_comfortable, degreesActivities[indexChosen])
        activation_rule3 = np.fmin(rule3, fit_decent)
    elif sortedIndices[2] == indexChosen: 
        rule2 = np.fmin(ratio_hasty, degreesActivities[indexChosen])
        activation_rule2 = np.fmin(rule2, fit_terrible)
        rule3 = np.fmin(ratio_comfortable, degreesActivities[indexChosen])
        activation_rule3 = np.fmin(rule3, fit_bad)
    elif sortedIndices[3] == indexChosen: 
        rule2 = np.fmin(ratio_hasty, degreesActivities[indexChosen])
        activation_rule2 = np.fmin(rule2, fit_terrible)
        rule3 = np.fmin(ratio_comfortable, degreesActivities[indexChosen])
        activation_rule3 = np.fmin(rule3, fit_terrible)
        
    # Aggregate all three output membership functions together
    aggregated = np.fmax(activation_rule1, np.fmax(activation_rule2, activation_rule3))
    return fuzz.defuzz(x_fit, aggregated, 'centroid')