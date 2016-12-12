import click
import numpy as np
import pandas as pd
import pdb
import skfuzzy as fuzz
from difflib import SequenceMatcher

@click.command()
@click.argument('data-filename')
@click.argument('labels-filename')
def cluster(data_filename, labels_filename):
	data = np.load(data_filename)
	labels = np.load(labels_filename)
	data = data[:,1:]
	clf = 	fuzz.cmeans(data, c=6, m=10, error=0.0001, maxiter=2000)
	filter_by_nutrients(list(labels))

def filter_by_nutrients(labels):
	test_labels = [u'Iron', u'Sodium', u'Fluoride', u'Selenium', u'Trans Fat', u'Phosphorus', u'Vitamin B2', u'Caffeine', u'Vitamin A', u'Vitamin B1', u'Mono Unsaturated Fat', u'Fiber', u'Vitamin K', u'Vitamin C', u'Sugar', u'Alcohol', u'Vitamin B3', u'Fat', u'Vitamin B6', u'Potassium', u'Cholesterol', u'Folate', u'Carbohydrates', u'Copper', u'Vitamin E', u'Vitamin B5', u'Saturated Fat', u'Manganese', u'Poly Unsaturated Fat', u'Calories', u'Zinc', u'Vitamin B12', u'Protein', u'Vitamin D', u'Magnesium', u'Calcium']
	filtered = []
	for label in labels:
		filtered.append(checkSimilarity(label, test_labels, filtered))

def checkSimilarity(nutrient, labels, filtered):
	for nutrition in labels:
		ratio = SequenceMatcher(None, nutrient, nutrition).ratio()
		if ratio > 0.5:
			if labels.index(nutrition) in filtered:
				continue
			else:
				return labels.index(nutrition)
	return -1


if __name__ == '__main__':
	cluster()
