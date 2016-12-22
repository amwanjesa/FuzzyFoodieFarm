import numpy as np
import skfuzzy as fuzz
import json
import unirest 
import pickle

colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']

# get the 500 random recipes
recipesNutrients = json.load(open("nutrientPercentages.txt"))

# all the important nutrients that is needed
all_keys = ['Caffeine', 'Calories', 'Carbohydrates', 'Cholesterol', 'Fat', 'Fiber', 'Protein', 'Saturated Fat', 'Sugar', 'Sodium', 'Iron', 'Vitamin A', 'Vitamin B1', 'Vitamin B2', 'Vitamin B3', 'Vitamin B5', 'Vitamin E']

def getNutrientsRecipes():
    # create the nutrition vectors for all the 500 random recipes 
    all_nutritions = []
    for nutritions in recipesNutrients: 
        vector = [nutritions[nut] if nut in nutritions else 0 for nut in all_keys]
        all_nutritions.append(vector)
    return np.matrix(all_nutritions)

# get membership degree of recipe for each cluster/activity   
def getPredictionNutrients(idRecipe): 
    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/" + idRecipe + "/information?includeNutrition=true"
    response = unirest.get(url,
      headers={
        "X-Mashape-Key": "uI9T1GTt8nmshcUUWJOjq8TQNGBgp1P9Zffjsn7dAbkmTSDt1k",
        "Accept": "application/json"
      }
    )
    recipeInfo = response.body
    # if recipe exists
    if 'nutrition' in recipeInfo:
        # get all of the nutrition information
        recipeNutritions = recipeInfo['nutrition']['nutrients']
        # create dict where each key is a nutrition and its value is the value of the nutrition
        nutritionsDict = {nutrition['title']: nutrition['percentOfDailyNeeds'] for nutrition in recipeNutritions}
        # create the nutrition vector with all of the nutrition keys so each element corresponds to the correct nutrition
        nutrition_vector = [nutritionsDict[nutrition] if nutrition in nutritionsDict else 0 for nutrition in all_keys]
        return np.matrix(nutrition_vector)
    else: 
        return 0

# clusters the given recipe and returns the membership degree for each cluster/activity
def testClustering(n_centers, m, idRecipe):
    test_data = getPredictionNutrients(idRecipe)
    # if recipe exists
    if type(test_data) != int:
        # get centers of the trained example
        with open('cluster.pkl', 'rb') as f:
            data = pickle.load(f)
        cntr = data[0]
        # predict one example
        u, u0, d, jm, p, fpc = fuzz.cluster.cmeans_predict(test_data.T, cntr, m, error=0.005, maxiter=1000)
        # get which cluster has the highest membership degree
        cluster_membership = np.argmax(u, axis=0)
        return cluster_membership, u
    else: 
        return 0