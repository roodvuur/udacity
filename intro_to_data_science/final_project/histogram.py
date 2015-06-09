import numpy as np
import pandas as pd
from matplotlib import pyplot

turnstile_weather = pd.read_csv('turnstile_master.csv')

def histogram_rain(pyplot):
	# Create two dataframes consisting of one colummn, ENTRIESn_hourly, one with rain and one without, the one without rain only including the first 80000 ENTRIESn_hourly
	# (Otherwise the histogram tail will grow very large)
	l1 = pd.DataFrame(turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 1]).sort(['ENTRIESn_hourly'])[:40000]
	l2 = pd.DataFrame(turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 0]).sort(['ENTRIESn_hourly'])[:80000]
	# Convert dataframes into lists
	l1 = l1['ENTRIESn_hourly'].tolist()
	l2 = l2['ENTRIESn_hourly'].tolist()
	# Convert lists into histograms
	pyplot.hist(l1, 50, alpha = 0.5, label = 'Rain')
	pyplot.hist(l2, 50, alpha = 0.5, label = 'No rain')

	return pyplot

def histogram_unit(pyplot):
	# Create dataframe with two columns, UNIT and ENTRIESn_hourly, group them by UNIT and then sum up all entries per group 
	df_subway_station = turnstile_weather.loc[:, ['UNIT', 'ENTRIESn_hourly']].groupby(['UNIT'], as_index = False).sum()
	# Make histogram
	pyplot.hist(df_subway_station['ENTRIESn_hourly'], 100)

	return pyplot

histogram_unit(pyplot).show()