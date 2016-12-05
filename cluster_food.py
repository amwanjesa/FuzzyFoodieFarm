import click
import numpy as np
import pandas as pd

@click.command()
@click.argument('data_filename')
def cluster(data_filename):
	df =  pd.read_csv(data_filename, dtype=str)
	numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
	newdf = df.select_dtypes(include=numerics)
	import pdb; pdb.set_trace()
	print df
	# data = []
	# names = []
	# for name in df.columns.values:
	# 	if containsNumbers(df[name]):
	# 		print df[name]
	# 		data.append(df[name])
	# 		names.append(name)
	# data = np.array(data)
	# names = np.array(names)
	# import pdb; pdb.set_trace()
	# np.save('food_facts', data)
	# np.save('fact_tags', names)

def containsNumbers(column):
	for i in column:
		if (isinstance(i, float) or isinstance(i, int)) and (not isinstance(i, str)):
			return True 
	return False
if __name__ == '__main__':
	cluster()
