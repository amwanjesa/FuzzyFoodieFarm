import click
import numpy as np
import pandas as pd
import pdb

@click.command()
@click.argument('data-filename')
@click.argument('output-filename')
def cluster(data_filename, output_filename):
	df =  pd.read_csv(data_filename, index_col=0, encoding='utf-8')
	df = df._get_numeric_data()
	df.to_csv(output_filename)

if __name__ == '__main__':
	cluster()
