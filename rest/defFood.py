import click
import pdb
import unirest
import pandas as pd
def foodList():
    recipes = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?diet=vegetarian&excludeIngredients=coconut&intolerances=egg%2C+gluten&limitLicense=false&number=10&offset=0&query=burger&type=main+course",
      headers={
        "X-Mashape-Key": "uI9T1GTt8nmshcUUWJOjq8TQNGBgp1P9Zffjsn7dAbkmTSDt1k",
        "Accept": "application/json"
      }
    )
    
    testData = recipes.body
    testFrame = pd.DataFrame(testData['results'], columns=['id', 'title', 'readyInMinutes'])
    #print(testFrame)
#    testFrame['fatPercentage'] = 3
    #print(testFrame)
#    fatP = satFatScale(str(testFrame.get('id')[i]),str(testFrame.get('title')[i]))
    testFrame['fatPercentage'] = testFrame.apply(satFatScale, axis = 1)
#    testFrame = pd.DataFrame(testData['results'], columns=['id', 'title', 'readyInMinutes', 'fatPercentage'])
    return testFrame   


def nutritions():
    response = unirest.get("https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/541691/information?includeNutrition=true",
      headers={
        "X-Mashape-Key": "uI9T1GTt8nmshcUUWJOjq8TQNGBgp1P9Zffjsn7dAbkmTSDt1k",
        "Accept": "application/json"
      }
    )
    recipeInfo = response.body
    
    selectedNutritions = ['Calories', 'Fat', 'Saturated Fat', 'Sugar']
    recipeNutritions = recipeInfo['nutrition']['nutrients']
    nutritionsDict = {nutrition['title']: nutrition['amount'] for nutrition in recipeNutritions if nutrition['title'] in selectedNutritions}
    nutritionsDict
    
    recipeNutritions = recipeInfo['nutrition']['ingredients']
    for ingredient in recipeNutritions:
        nutrients = ingredient['nutrients']
        ingrNutritions = [nut['name'] for nut in nutrients]
        #print len(ingrNutritions)
    print(ingrNutritions)

def satFatScale(num):
    num = str(num['id'])
    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"+num+"/information?includeNutrition=true"
    response = unirest.get(url,
      headers={
        "X-Mashape-Key": "uI9T1GTt8nmshcUUWJOjq8TQNGBgp1P9Zffjsn7dAbkmTSDt1k",
        "Accept": "application/json"
      }
    )
    recipeInfo = response.body

    selectedNutritions = ['Calories', 'Fat', 'Saturated Fat', 'Sugar', 'Fiber']
    recipeNutritions = recipeInfo['nutrition']['nutrients']
    nutritionsDict = {nutrition['title']: nutrition['amount'] for nutrition in recipeNutritions if nutrition['title'] in selectedNutritions}
#    print(num, nutritionsDict.get('Saturated Fat')*9/nutritionsDict.get('Calories')*100)
    return round(nutritionsDict.get('Saturated Fat')*9/nutritionsDict.get('Calories')*100)

print(foodList())
#nutritions()