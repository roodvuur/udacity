from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.examples

def most_tweets(db):
	
	result = db.twitter.aggregate([
		{'$group' : {'_id' : '$user.screen_name',
					'count' : {'$sum' : 1},
					'tweet_texts' : {'$push' : '$text'}}},
		{'$project' : {'_id' : '$_id', 'count' : '$count', 'tweet_texts' : '$tweet_texts'}},
		{'$sort' : {'count' : -1}},
		{'$limit': 5}
	])

	for r in result:
		pprint.pprint(r)

most_tweets(db)