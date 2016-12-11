import click
import numpy as np
import pandas as pd
import pdb
import skfuzzy as fuzz

@click.command()
@click.argument('data-filename')
def cluster_n_predict(data_filename):
	data = np.load(data_filename)
	data = data[:,1:]
	clf = 	fuzz.cmeans(data, c=6, m=0.01, error=0.0001, maxiter=2000)
	classified = []
	for ingredients in recipe:
		prediction = fuzz.cmeans_predict(ingredients, clf.cntr)
		classified.append(prediction)

if __name__ == '__main__':
	cluster()
