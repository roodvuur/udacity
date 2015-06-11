import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = open('./data/pittsburgh.osm', 'r')

# Establish the regular expression for extracting street type, and create
# a dictionary with default value int
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
street_types = defaultdict(int)

def autdit_street_type(street_types, street_name):

	"""
	Extract and count street types from street names
	"""
	# Search the street name for given expression
	m = street_type_re.search(street_name)
	if m:
		# Increase count of this type of street
		street_type = m.group()
		street_types[street_type] += 1

def print_sorted_dict(d):

	"""
	Print a dictionary d, sorted by key 
	"""
	# Get dictionary keys, sort them and convert to lowercase if neccessary
	keys = d.keys()
	keys = sorted(keys, key = lambda s: s.lower())
	# Loop trough keys and print it out with its corresponding value
	for k in keys:
		v = d[k]
		print '{}: {}'.format(k, v)

def is_street_name(elem):

	"""
	Check if XML element contains street name
	"""
	# Return True if element is tag, and has the attribute k w/ value addr:street
	return (elem.tag == 'tag') and (elem.attrib['k'] == 'addr:street')

def audit():
	"""
	Audit all data 
	"""

	# Loop through all xml elements
	for event, elem in ET.iterparse(osm_file):
		# If a street name, autdit its type
		if is_street_name(elem):
			autdit_street_type(street_types, elem.attrib['v'])
	# Print all street types
	print_sorted_dict(street_types)

audit()

