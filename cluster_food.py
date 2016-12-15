import click
import numpy as np
import pandas as pd
import pdb
import skfuzzy as fuzz
from difflib import SequenceMatcher
from nutrition import nutritions
import matplotlib.pyplot as plt
import simplejson as json

colors = ['b', 'orange', 'g', 'r', 'c', 'm', 'y', 'k', 'Brown', 'ForestGreen']


@click.command()
@click.argument('data-filename')
@click.argument('labels-filename')
def cluster(data_filename, labels_filename):
	data = np.load(data_filename)
	labels = np.load(labels_filename)
	data = data[:,1:]
	clf = fuzz.cmeans(data, c=6, m=10, error=0.0001, maxiter=2000)
	recipe_labels = json.load(open("recipesNutrients.txt"))
	nutritions = []
	for recipe in recipe_labels:
		nutrient_vector = filter_by_nutrients(list(labels), recipe)
		nutritions.append(nutrient_vector)

	testClustering(data, np.array(nutritions).T)


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

def testClustering(train_data, test_data):
	m = 1.1
	ncenters = 6

	cntr_train, u_train, u0, d, jm, p, fpc = fuzz.cluster.cmeans(train_data, ncenters, m, error=0.005, maxiter=1000, init=None)

	cluster_membership = np.argmax(u_train, axis=0)

	for x in range(ncenters):
		plt.plot()
		# import pdb; pdb.set_trace()
		plt.plot(test_data[cluster_membership == x], test_data[cluster_membership == x],'.', color=colors[x])

	plt.title('Centers = {0}; FPC = {1:.2f}'.format(ncenters, fpc))
	plt.axis('off')



	plt.show()

if __name__ == '__main__':
	clf, nutrient_vector, data = cluster()
