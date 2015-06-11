from bs4 import BeautifulSoup
from string import *
import json
import requests

html_page = 'html_page.html'

def extract_carriers(page):
	data = []

	with open(page, 'r') as html:
		# Load html document in soup variable
		soup = BeautifulSoup(html)
		# Set clist to the select element in page
		clist = soup.find('select', id = 'CarrierList')
		# Loop through all options (airlines)
		for option in clist.find_all('option'):
			# Check if option is not aggregate
			if option['value'].startswith('All'):
				continue
			data.append(option['value'])
	return data

def extract_airports(page):
	data = []

	with open(page, 'r') as html:
		# Load html document in soup variable
		soup = BeautifulSoup(html)
		# Set clist to the select element in page
		clist = soup.find('select', id = 'AirportList')
		# Loop through all options (airlines)
		for option in clist.find_all('option'):
			# Check if option is not aggregate
			if option['value'].startswith('All'):
				continue
			data.append(option['value'])
	return data

def extract_data(page, session):
	# Setup data dictionary, get html in BS object
	data = {"eventvalidation": "",
	        "viewstate": ""}
	html = session.get(page).text
	soup = BeautifulSoup(html)
	# Find appropriate values and assign them to data
	data['viewstate'] = soup.find('input', id = '__VIEWSTATE')['value']
	data['eventvalidation'] = soup.find('input', id = '__EVENTVALIDATION')['value']
	
	return data


def make_request(data, session, combo):
	# Setup variables
	eventvalidation = data["eventvalidation"]
	viewstate = data["viewstate"]
	# Make post request to session with proper data
	r = session.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': combo['airport'],
                          'CarrierList': combo['carrier'],
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                	})

   	return r.text

# Set page url
page = 'http://www.transtats.bts.gov/Data_Elements.aspx?Data=2'
# Create a dictionary of carriers & airports
combo = {'carriers' : extract_carriers(html_page), 'airports' : extract_airports(html_page)}
# Create session object & extract data neccessary to perform post request
s = requests.Session()
data = extract_data(page, s)

# Loop through all carriers
for c in combo['carriers']:
	# Then through all aiports
	for a in combo['airports']:
		# Get html file and save
		f = make_request(data, s, {'carrier' : c, 'airport' : a})
		target = open('./data/'+c+'-'+a+'.html', 'w')
		target.write(f)
		target.close()
