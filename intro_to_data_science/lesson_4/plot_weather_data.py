from pandas import *
from ggplot import *
import numpy as np

def plot_weather_data(turnstile_weather):
	"""
	Plot turnstile weather data
	"""

	# Subway ridership by time of day
	# Create pivot table with UNIT on one hand, and cummulative entries on the other
	df_time_of_day = turnstile_weather.loc[:, ['Hour', 'ENTRIESn_hourly']].groupby(['Hour'], as_index = False).sum()
	# Create plot
	df_time_of_day_plot = ggplot(df_time_of_day, aes('Hour'))
	df_time_of_day_plot = df_time_of_day_plot + geom_bar(aes(x = 'Hour', weight = 'ENTRIESn_hourly'), binwidth = 1) + scale_x_continuous(limits = (0, 23))

	# Subway ridership by subway station
	# Create pivot table with UNIT on one hand, and cummulative entries on the other
	df_subway_station = turnstile_weather.loc[:, ['UNIT', 'ENTRIESn_hourly']].groupby(['UNIT'], as_index = False).sum()
	# Create plot
	df_subway_station_plot = ggplot(df_subway_station, aes(x = 'UNIT'))
	df_subway_station_plot = df_subway_station_plot + geom_bar(aes(x = 'UNIT', weight ='ENTRIESn_hourly'))

	# Subway ridership, total
	# Create pivot table with DATEn on one hand, and entries on the other
	df_total = turnstile_weather.loc[:, ['DATEn', 'ENTRIESn_hourly']].groupby(['DATEn'], as_index = False).sum()
	# Convert DATEn column to proper datetime
	df_total['DATEn'] = pandas.to_datetime(df_total['DATEn'])
	df_total['DATEn'] = [d.date() for d in df_total['DATEn']]
	# Create plot
	df_total_plot = ggplot(df_total, aes('DATEn'))
	df_total_plot = df_total_plot + geom_bar(aes(x = 'DATEn', weight = 'ENTRIESn_hourly')) + scale_x_date()

	return df_time_of_day_plot, df_subway_station_plot, df_total_plot

data = 'turnstile_master.csv'
df = read_csv(data)
tof, ss, tt = plot_weather_data(df)
print tt