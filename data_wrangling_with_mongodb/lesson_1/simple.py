import os

DATADIR = ''
DATAFILE = 'beatles-diskography.csv'
delimiter = ','

def parse_file(datafile):
	# List to hold all our dictionaries
	data = []
	# Open csv file
	with open(datafile, 'r') as f:
		# Labels list
		labels = f.readline().split(delimiter)
		e = 0
		for line in f:
			if e == 10:
				break
			# Split each line by delimiter
			line_data = line.strip().split(delimiter)
			# Create dictionary
			dic = {}
			for i, value in enumerate(line_data):
				dic[labels[i]] = line_data[i]
			# Add dictionary to data
			data.append(dic)
			e+=1
			
	return data

def test():
	# a simple test of your implemetation
	datafile = os.path.join(DATADIR, DATAFILE)
	d = parse_file(datafile)
	print d
	firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
	tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

	assert d[0] == firstline
	assert d[9] == tenthline

    
test()

