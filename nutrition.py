import click
import pdb
import unirest
import pandas as pd 


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
	print nutritionsDict

if __name__ == '__main__':
	nutritions(); 