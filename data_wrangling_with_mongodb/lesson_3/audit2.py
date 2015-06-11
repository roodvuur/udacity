import codecs
import csv
import json
import pprint

pp = pprint.PrettyPrinter(indent = 4)

CITIES = './data/cities.csv'
FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]

# Helper function to determine wether value is integer or float
def is_integer(value):
	try:
		int(value)
		return True
	except ValueError:
		return False

def is_float(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

def audit_file(filename, fields):

	"""
	Returns a dictionary of the fields and the occuring datatypes
	"""

	fieldtypes = {}

	# Open csv file
	with open(filename, 'r') as f:
		# Populate fieldtypes with all the field
		for field in fields:
			fieldtypes[field] = set()
		reader = csv.reader(f, delimiter = ',')
		header = []
		for i, row in enumerate(reader):
			# Store header
			if i == 0:
				header = row
				continue
			# Discard other, weird rows
			if i in range(1, 4):
				continue
			# For each field, check which datatype is present and store it in the 
			# fieldtypes dictionary
			for i, field in enumerate(row):
				# Check which datafield we're working with
				datafield = header[i]
				# If datafield not in datafields, stop working
				if not datafield in fields:
					continue
				datatype = ''
				# Check for values
				if field == 'NULL' or field == '':
					datatype = type(None)
				elif field.startswith('{'):
					datatype = type([])
				elif is_integer(field):
					datatype = type(1)
				elif is_float(field):
					datatype = type(1.1)
				else:
					datatype = type('hello')
				# Check fieldtypes dict to see if this datatype is already in set
				if not datatype in fieldtypes[datafield]:
					fieldtypes[datafield].add(datatype)

	return fieldtypes

def fix_area(area):

	"""
	Returns 'fixed' area in case area consist of array, unchanged area otherwise
	"""

	# Check wether area is float (or int), if so, return its value
	if is_float(area):
		return area
	# Next, determine wether area is an array. If it's not, and it's not float either,
	# it has to be invalid
	elif not area.startswith('{'):
		return None
	# Knowing area is an array, get its values
	area_split = area.split('|')
	# We can safely ignore the first and last characters
	value1 = area_split[0][1:].strip()
	value2 = area_split[1][:len(area_split[1]) - 1].strip()
	# Keep the value with the most amount of digits
	if len(value1) > len(value2):
		return float(value1)
	else:
		return float(value2)

def fix_name(name):

	"""
	Return a list of names. If one present, the list will only contain one item. If
	NULL, it returns an empty list
	"""

	lis = []

	# Check wether array
	if not name.startswith('{'):
		# Not an array, return empty list if null, list with name otherwise
		if name == 'NULL':
			return lis
		else:
			lis.append(name)
			return lis
	# We know name is an array. Extract values.
	name_split = name[1:(len(name) - 1)].split('|')
	# Iterate over names, add each name to list and finally return list
	for n in name_split:
		lis.append(n)
	return lis

def check_loc(point, lat, longi):

	"""
	Return true if point is consistent with lattitude and longitude, false otherwise
	"""

	# Split point into assumed lat and longi, check values and return appropriately
	point_split = point.split(' ')
	if point_split[0] != lat:
		return False
	elif point_split[1] != longi:
		return False
	else:
		return True
