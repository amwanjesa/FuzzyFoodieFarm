import click
import numpy as np
import pandas as pd

@click.command()
@click.argument('data_filename')
def cluster(data_filename):
	df =  pd.read_csv(data_filename, dtype=str)
	data = []
	names = []
	for name in df.columns.values:
		if containsNumbers(df[name]):
			data.append(df[name])
			names.append(name)
	np.save('food_facts', np.array(data))
	np.save('fact_tags', np.array(names))

def containsNumbers(column):
	for i in column:
		if isinstance(i, float) or isinstance(i, int):
			return True
	return False
if __name__ == '__main__':
	cluster()
