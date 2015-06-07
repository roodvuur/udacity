import pandas
from ggplot import *

def lineplot_compare(hr_by_team_year_sf_la_csv):
	"""
	Show a lineplot comparing the homeruns per team (SF, LA)
	"""

	# Read csv file
	df = pandas.read_csv(hr_by_team_year_sf_la_csv)

	# Create plot
	gg = ggplot(df, aes('yearID', 'HR', color='teamID')) + geom_point() + geom_line()

	# Show plot
	print gg

data = 'hr_by_team_year_sf_la.csv'
print lineplot_compare(data)