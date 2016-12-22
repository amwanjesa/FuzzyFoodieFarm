import numpy as np
import skfuzzy as fuzz
import heapq

def defuzzify(ratio_degrees, u, activities, chosen):
    
    # assign the membership degrees to the fuzzy sets of ratio
    ratio_comfortable = ratio_degrees[0]
    ratio_hasty = ratio_degrees[1]
    ratio_impossible = ratio_degrees[2]
 
    # assign the membership degrees to the fuzzy sets of activities   
    activity_postworkout = u[0]
    activity_study = u[1]
    activity_life = u[2]
    activity_sport = u[3]
    
    # create the universe of the output: fit    
    x_fit = np.arange(0, 1.1, 0.1)
    
    # assign the membership functions for the outpu
    fit_terrible = fuzz.trapmf(x_fit, [0, 0, 0.25, 0.375])
    fit_bad = fuzz.trapmf(x_fit, [0.25, 0.375, 0.5, 0.675])
    fit_decent = fuzz.trapmf(x_fit, [0.5, 0.675, 0.75, 0.875])
    fit_good = fuzz.trapmf(x_fit, [0.75, 0.875, 1, 1])
    
    # get the index of which activity is chosen
    indexChosen = activities.index(chosen)
    
    # create list for the degrees of activity
    degreesActivities = [activity_postworkout, activity_study, activity_life, activity_sport]

    # first rule: if ratio is impossible then fit is terrible
    activation_rule1 = np.fmin(ratio_impossible, fit_terrible)

    # get the indices in sorted manner depending on the value of degree per activity
    sortedIndices = heapq.nlargest(4, xrange(len(degreesActivities)), key=degreesActivities.__getitem__)
    
    # if the chosen activity has the highest membership degree for this recipe
    if sortedIndices[0] == indexChosen: 
        # if ratio is hasty and activity is chosen activity then fit is decent
        rule2 = np.fmin(ratio_hasty, degreesActivities[indexChosen])
        # implication
        activation_rule2 = np.fmin(rule2, fit_decent)
        # if ratio is comfortable and activity is chosen activity then fit is good
        rule3 = np.fmin(ratio_comfortable, degreesActivities[indexChosen])
        activation_rule3 = np.fmin(rule3, fit_good)
        
    # if the chosen activity has the second highest membership degree for this recipe
    elif sortedIndices[1] == indexChosen: 
        rule2 = np.fmin(ratio_hasty, degreesActivities[indexChosen])
        activation_rule2 = np.fmin(rule2, fit_bad)
        rule3 = np.fmin(ratio_comfortable, degreesActivities[indexChosen])
        activation_rule3 = np.fmin(rule3, fit_decent)
    
    # if the chosen activity has the third highest membership degree for this recipe
    elif sortedIndices[2] == indexChosen: 
        rule2 = np.fmin(ratio_hasty, degreesActivities[indexChosen])
        activation_rule2 = np.fmin(rule2, fit_terrible)
        rule3 = np.fmin(ratio_comfortable, degreesActivities[indexChosen])
        activation_rule3 = np.fmin(rule3, fit_bad)
    
    # if the chosen activity has the fourth highest membership degree for this recipe
    elif sortedIndices[3] == indexChosen: 
        rule2 = np.fmin(ratio_hasty, degreesActivities[indexChosen])
        activation_rule2 = np.fmin(rule2, fit_terrible)
        rule3 = np.fmin(ratio_comfortable, degreesActivities[indexChosen])
        activation_rule3 = np.fmin(rule3, fit_terrible)
        
    # aggregate all three output membership functions together
    aggregated = np.fmax(activation_rule1, np.fmax(activation_rule2, activation_rule3))
    # return defuzzification value
    return fuzz.defuzz(x_fit, aggregated, 'centroid')