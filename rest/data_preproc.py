import click
import numpy as np
import pandas as pd

@click.command()
@click.argument('data-filename')
@click.argument('output-filename')
def preprocess(data_filename, output_filename):


	df =  pd.read_csv(data_filename, index_col=0, encoding='utf-8')

	#all nutrition data in numeric
	df = df._get_numeric_data()

	#fill not-a-number values with 0
	df = df.fillna(0)

	#save the labels for later matching to recipe ingredients' nutreints
	np.save('labels', df.columns.values)
	np.save(output_filename, df.as_matrix())

if __name__ == '__main__':
	preprocess()
