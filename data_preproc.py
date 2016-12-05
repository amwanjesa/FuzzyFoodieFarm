import click
import numpy as np
import pandas as pd

@click.command()
@click.argument('data-filename')
@click.argument('output-filename')
def preprocess(data_filename, output_filename):
	df =  pd.read_csv(data_filename, index_col=0, encoding='utf-8')
	df = df._get_numeric_data()
	df = df.fillna(0)
	np.save(output_filename, df.as_matrix())

if __name__ == '__main__':
	preprocess()
