from pandas import *
from ggplot import *
import numpy as np

def plot_weather_data(turnstile_weather):
	"""
	Plot turnstile weather data
	"""

	# Create new dataframe consisting of hours and corresponding frequencies
	df_time_of_day = pivot_table(data = turnstile_weather, index = 'Hour', values=['ENTRIESn_hourly'], aggfunc = np.sum) 
	df_time_of_day_plot = ggplot(df_time_of_day.reset_index(), aes('Hour', 'ENTRIESn_hourly'))
	df_time_of_day_plot = df_time_of_day_plot + geom_bar(stat='bar') + scale_x_discrete(limits = (0, 23))

	# Create pivot table with UNIT on one hand, and cummulative entries on the other
	df_subway_station = pivot_table(data = turnstile_weather, index = 'UNIT', values=['ENTRIESn_hourly'], aggfunc = np.sum) 
	# We cannot use the unit name as x value yet, thus we have to create another column with integers corresponding to different units
	df_subway_station = df_subway_station.reset_index()
	df_subway_station.index.name = 'UNIT_integer'
	print df_subway_station
	# Create plot
	df_subway_station_plot = ggplot(df_subway_station.reset_index(), aes(x = 'UNIT_integer', y = 'ENTRIESn_hourly'))
	df_subway_station_plot = df_subway_station_plot + geom_histogram(stat = 'identity') + scale_x_discrete(limits = (0, 470))

	return df_subway_station_plot

data = 'turnstile_master.csv'
df = read_csv(data)
p = plot_weather_data(df)
print p