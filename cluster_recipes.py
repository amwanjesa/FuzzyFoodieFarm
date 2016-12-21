import numpy as np
import skfuzzy as fuzz
import json
import unirest

colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']

# get the 500 random recipes
recipesNutrients = json.load(open("recipesNutrients.txt"))
# all the important nutrients that is needed
all_keys = ['Caffeine', 'Calories', 'Carbohydrates', 'Cholesterol', 'Fat', 'Fiber', 'Protein', 'Saturated Fat', 'Sugar', 'Sodium', 'Iron', 'Vitamin A', 'Vitamin B1', 'Vitamin B2', 'Vitamin B3', 'Vitamin B5', 'Vitamin E']

def getNutrientsRecipes():
    # create the nutrition vectors for all the 100 random recipes
    all_nutritions = []
    for nutritions in recipesNutrients:
        vector = [nutritions[nut] if nut in nutritions else 0 for nut in all_keys]
        all_nutritions.append(vector)
    return np.matrix(all_nutritions)

def getPredictionNutrients(idList):
    nutrition_matrix = []
    for idRecipe in idList:
        idRecipe = str(idRecipe)
        url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/" + idRecipe + "/information?includeNutrition=true"
        response = unirest.get(url,
          headers={
            "X-Mashape-Key": "uI9T1GTt8nmshcUUWJOjq8TQNGBgp1P9Zffjsn7dAbkmTSDt1k",
            "Accept": "application/json"
          }
        )
        recipeInfo = response.body
        # get all of the nutrition information
        recipeNutritions = recipeInfo['nutrition']['nutrients']
        # create dict where each key is a nutrition and its value is the value of the nutrition
        nutritionsDict = {nutrition['title']: nutrition['amount'] for nutrition in recipeNutritions}# if nutrition['title'] in selectedNutritions}
        # create the nutrition vector with all of the nutrition keys so each element corresponds to the correct nutrition
        # this is for the one prediction example
        nutrition_vector = [nutritionsDict[nutrition] if nutrition in nutritionsDict else 0 for nutrition in all_keys]
        nutrition_matrix.append(nutrition_vector)
    return np.matrix(nutrition_matrix)

#The function below tests clustering the data
def testClustering(n_centers, m, idList):
    training_data = getNutrientsRecipes()
    test_data = getPredictionNutrients(idList)
    # train the 100 examples
    cntr, u_train, u0_train, d, jm, p, fpc = fuzz.cluster.cmeans(training_data.T, n_centers, m, error=0.005, maxiter=1000, init=None)
    # predict one example
    u, u0, d, jm, p, fpc = fuzz.cluster.cmeans_predict(test_data.T, cntr, m, error=0.005, maxiter=1000)
    # get to which cluster the example belongs to
    cluster_membership = np.argmax(u, axis=0)  # Hardening for visualization
    return cluster_membership
