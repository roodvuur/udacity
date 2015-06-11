import csv
import pprint
import datetime

INPUT_FILE =  './data/autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

pp = pprint.PrettyPrinter(indent = 4)

def process_file(input_file, output_good, output_bad):

	"""
	Verify the validity of production year
	"""
	# Lists containing good and bad rows
	list_good = []
	list_bad = []
	# Open csv file 
	with open(input_file, 'r') as f:
		# Create reader from csv and store header row
		reader = csv.DictReader(f)
		header = reader.fieldnames
		# Store useful keys
		year = 'productionStartYear'
		uri = 'URI'
		# Loop through all rows
		for row in reader:
			# Discard rows with a URI not from DBpedia
			if not row[uri].startswith('http://dbpedia.org'):
				continue
			# Extract year from datetime
			year_value = row[year][:4]
			# Change row datetime value to its year
			row[year] = year_value
			# Check if year actually contains a year
			if not row[year].isdigit():
				# Add to list_bad
				list_bad.append(row)
				continue
			# Check if year falls within expected range
			if int(row[year]) < 1886 or int(row[year]) > 2014:
				# Add list to bad
				list_bad.append(row)
				continue
			# Row is proper, add to list_good
			list_good.append(row)
		
		# Open good ouput file, write the good rows to it
		with open(output_good, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, delimiter = ',', fieldnames = header)
			writer.writeheader()
			for item in list_good:
				writer.writerow(item)

		# Open bad ouput file, write the nad rows to it
		with open(output_bad, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, delimiter = ',', fieldnames = header)
			writer.writeheader()
			for item in list_bad:
				writer.writerow(item)
		
process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)