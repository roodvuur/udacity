import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy
import scipy.stats
import pandas
from ggplot import *
from random import sample

def mann_whitneyu(sample1, sample2):
	"""
	Do the Mann-Whitney U-test and return the U-value and p-value
	"""

	U, p = scipy.stats.mannwhitneyu(sample1, sample2)

	return U, p 

def normalize_features(df):
	"""
	Normalize the features in a dataframe
	"""

	# Calculate mean & standard deviation
	mu = df.mean()
	sigma = df.std()

	# Check if one or more of the features has standard deviation zero, everywhere
	# If so, raise an error because we cannot make predictions if a feature is the same
	# for every value
	if (sigma == 0).any():
		raise Exception("One or more values has standard deviation zero everywhere. Please correct.")
	# Substract mean from dataframe (shift to zero)
	df = df - mu
	# Devide by sigma (list features in terms of standard deviations instead of absolute numbers)
	df = df / sigma

	return df, mu, sigma

def compute_r_squared(values, features, theta):
	"""
	Compute r squared, a measure of how much correlatione exists between our predictor variables
	and our independent variable
	"""

	# Calculate predicted values
	predicted = np.dot(features, theta)
	# Calculate predicted values mean
	mu = np.mean(values)
	# Calculate numerator and denominator
	numerator = np.square(values - predicted).sum()
	denominator = np.square(values - mu).sum()
	# Calculate r squared
	r_squared = 1 - (numerator/denominator)

	return r_squared

def compute_cost(values, features, theta):
	"""
	Compute cost for a given set of thetas
	"""

	m = len(values)

	# Calculate intermediate value, the sum of squares
	intermediate = (np.square(np.dot(features, theta) - values)).sum()
	# Calculate cost as the sum of squares times half the amount of values
	cost = intermediate / (2 * m)
	return cost

def gradient_descent(values, features, theta, alpha, num_iterations):
	"""
	Perform gradient descent
	"""

	# Gradient descent updates the theta values so that it influences the cost function in such a way that
	# , all else equal, it will return a lower value. It moves the 'x' value towards the line's steepest descent

	cost_history = []
	m = len(values)
	# Loop num_iterations times
	for i in range(num_iterations):
		# Calculate derivative of the cost function (compute_cost)
		predicted = np.dot(features, theta)
		ddxcost = np.dot((predicted - values), features)
		# Calculate our new theta
		theta = theta - (alpha / m) * ddxcost
		# Get cost
		cost = compute_cost(values, features, theta)
		# Append cost to cost_history
		cost_history.append(cost)

	return theta, pandas.Series(cost_history)

def predictions(df):
	"""
	Make predictions about our data using numerous functions in this document
	"""
	# Set features
	features = df[['rain', 'meanwindspdi', 'Hour', 'maxtempi']]

	# Convert categorical UNIT variables into numerical dummy variables
	#dummy_units = pandas.get_dummies(df['UNIT'], prefix='unit')
	#features = features.join(dummy_units)

	# Get observed values
	values = df['ENTRIESn_hourly']

	# Normalize features
	features, mu, sigma = normalize_features(features)

	# Add a column of ones to features
	features['ones'] = np.ones(len(values))

	# Convert features, values to NumPy arrays
	features_array = np.array(features)
	values_array = np.array(values)

	# Set values for num_iterations and alpha
	num_iterations = 100
	alpha = 0.5

	# Initiazize theta and perform gradient descent
	theta_gradient_descent = np.zeros(len(features.columns))
	theta_gradient_descent, cost_history = gradient_descent(values_array, features_array, theta_gradient_descent, alpha, num_iterations)

	# Make predictions
	predictions = np.dot(features_array, theta_gradient_descent)
	# Calculate r squared
	r_squared = compute_r_squared(values, features, theta_gradient_descent)
	# Create cost history plot
	plot = None
	#plot = plot_cost_history(alpha, cost_history)
	return predictions, plot, theta_gradient_descent

def predictions_ols(df):
	"""
	Make predictions about the subway ridership based on predictions_ols
	"""
	# Set features
	features = df[['rain', 'meanwindspdi', 'Hour', 'maxtempi']]

	# Convert categorical UNIT variables into numerical dummy variables
	#dummy_units = pandas.get_dummies(df['UNIT'], prefix='unit')
	#features = features.join(dummy_units)

	# Get observed values
	values = df['ENTRIESn_hourly']

	# Normalize features
	features, mu, sigma = normalize_features(features)

	# Add a column of ones to features
	features['ones'] = np.ones(len(values))

	model = sm.OLS(values, features)
	results = model.fit()

	predictions = np.dot(features, results.tvalues)

	return predictions, results

def plot_cost_history(alpha, cost_history):
	"""
	Plot the cost history
	"""
	cost_df = pandas.DataFrame({
		'Cost_History': cost_history,
    	'Iteration': range(len(cost_history))
	})
	return ggplot(cost_df, aes('Iteration', 'Cost_History')) + geom_point() + geom_line() + ggtitle('Cost History for alpha = %.3f' % alpha )

def plot_residuals(turnstile_weather, predictions):
	plt.figure()
	(turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins=150)
	return plt

# Read master CSV file
csv = pandas.read_csv('turnstile_master.csv')
# Create an NumPy array of sample_size numbers, all between 0 and the amount of rows in our master csv
sample_size = 10000
index = np.array(sample(range(len(csv)), sample_size))
# Pick rows corresponding to the random index list from master csv and store in our dataframe
df = csv.ix[index]

# Make predictions
p2, plot, theta = predictions(df)
p1, results = predictions_ols(df)

# Compare the two predictions
U, p = mann_whitneyu(p1, p2)

print results.tvalues
print results.rsquared
print theta