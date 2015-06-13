#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a list of dictionaries of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc. If there is a singular synonym, the value should still be formatted
  in a list.
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
					'family': 'Orb-weaver spider',
					'class': 'Arachnid',
					'phylum': 'Arthropod',
					'order': 'Spider',
					'kingdom': 'Animal',
					'genus': None
					}
}
  * Note that the value associated with the classification key is a dictionary with
	taxonomic labels.
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
		 'URI': 'uri',
		 'rdf-schema#comment': 'description',
		 'synonym': 'synonym',
		 'name': 'name',
		 'family_label': 'family',
		 'class_label': 'class',
		 'phylum_label': 'phylum',
		 'order_label': 'order',
		 'kingdom_label': 'kingdom',
		 'genus_label': 'genus'}


def process_file(filename, fields):

	process_fields = fields.keys()
	data = []
	with open(filename, "r") as f:
		reader = csv.DictReader(f)
		header = reader.fieldnames
		for i in range(3):
			l = reader.next()
		for row in reader:
			prelim_data = {}
			prelim_data['classification'] = {}
			for val in row:
				# Check if we must process this field
				if val in FIELDS:
					# Start cleaning
					if val == 'name' and (row[val] == 'NULL' or re.match(r'\W+', row[val])):
						row[val] = row['rdf-schema#label']
					if row[val] == 'NULL':
						row[val] = None
					elif val == 'rdf-schema#label':
						i = row[val].split('(')
						if len(i) > 1:
							row[val] = i[0]
					if val == 'synonym' and row[val] != None:
						a = None
						if row[val].startswith('{'):
							a = parse_array(row[val])
						elif row[val] != 'synonym'and row[val] != 'NULL':
							a = []
							a.append(row[val])
						if a != None:
							for z, b in enumerate(a):
								a[z] = b.replace('*', '').strip()
						row[val] = a
				# Trim whitespace from start and end of value
				t = True
				while(t):
					if type(row[val]) == type([]) or row[val] == None:
						t = False
						continue
					if row[val].startswith(' '):
						row[val] = row[val][1:]
					elif row[val].endswith(' '):
						row[val] = row[val][:len(row[val])-1]
					else:
						t = False
				# Assign to the correct dictionary with correct labels
				for field in FIELDS:
					if val == field:
						# In the special case of classification field, processs properly
						if val in ['family_label', 'class_label', 'phylum_label', 'kingdom_label', 'genus_label', 'order_label']:
							prelim_data['classification'][FIELDS[field]] = row[val]
						else:
							prelim_data[FIELDS[field]] = row[val]
			data.append(prelim_data)

	return data


def parse_array(v):
	if (v[0] == "{") and (v[-1] == "}"):
		v = v.lstrip("{")
		v = v.rstrip("}")
		v_array = v.split("|")
		v_array = [i.strip() for i in v_array]
		return v_array
	return [v]


def test():
	data = process_file(DATAFILE, FIELDS)
	print "Your first entry:"
	pprint.pprint(data[0])
	print len(data)
	first_entry = {
		"synonym": None, 
		"name": "Argiope", 
		"classification": {
			"kingdom": "Animal", 
			"family": "Orb-weaver spider", 
			"order": "Spider", 
			"phylum": "Arthropod", 
			"genus": None, 
			"class": "Arachnid"
		}, 
		"uri": "http://dbpedia.org/resource/Argiope_(spider)", 
		"label": "Argiope", 
		"description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
	}
	assert len(data) == 76
	assert data[0] == first_entry
	assert data[17]["name"] == "Ogdenia"
	assert data[48]["label"] == "Hydrachnidiae"
	assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == "__main__":
	test()