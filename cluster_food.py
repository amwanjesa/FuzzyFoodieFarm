import click
import numpy as np
import pandas as pd
import pdb
import skfuzzy as fuzz
from difflib import SequenceMatcher
from nutrition import nutritions

@click.command()
@click.argument('data-filename')
@click.argument('labels-filename')
def cluster(data_filename, labels_filename):
	data = np.load(data_filename)
	labels = np.load(labels_filename)
	data = data[:,1:]
	clf = 	fuzz.cmeans(data, c=6, m=10, error=0.0001, maxiter=2000)
	recipe_labels = nutritions()
	nutrient_vector = filter_by_nutrients(list(labels), recipe_labels)

def filter_by_nutrients(labels, recipe):
	recipe_labels = recipe.keys()
	filtered = []
	for label in labels:
		filtered.append(checkSimilarity(label, recipe_labels, filtered))
	nutrient_vector = []
	for index in filtered:
		if isinstance(index, str) or isinstance(index, unicode):
			nutrient_vector.append(recipe[index])
		else:
			nutrient_vector.append(0)
	return nutrient_vector

def checkSimilarity(nutrient, labels, filtered):
	for nutrition in labels:
		ratio = SequenceMatcher(None, nutrient, nutrition).ratio()
		if ratio > 0.5:
			if nutrition in filtered:
				continue
			else:
				return nutrition
	return -1


if __name__ == '__main__':
	cluster()
