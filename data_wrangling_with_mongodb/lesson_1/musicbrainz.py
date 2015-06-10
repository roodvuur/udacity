import json
import requests

BASE_URL = 'http://musicbrains.org/ws/2/'
ARTIST_URL = BASE_URL + 'artist/'

query_type = {'simple': {}, 'atr': {'inc' : 'aliases+tags+ratings'}, 'releases' : {'inc' : 'releases'}}

def query_site(url, params, uid='', fmt='json'):
	params['fmt'] = fmt
	r = requests.get(url + uid, params=params)

	if r.status_code == requests.codes.ok:
		print 'All well'
		return r.json()
	else:
		print 'All bad'
		r.raise_for_status()

def query_by_name(url, params, name):
	params['query'] = 'artist:'+name
	return query_site(url, params)

def query():
	results = query_by_name(ARTIST_URL, query_type['simple'], name='FIRST AID KIT')
	for r in results['artists']:
		pretty_print(r)

def pretty_print(data, indent=4):
	if type(data) == dict:
		print 'dict'
		print json.dumps(data, indent=indent, sort_keys=True)
	else:
		print 'data'
		print data

query()