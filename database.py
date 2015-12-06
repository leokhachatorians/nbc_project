import pymongo
import json
import bson

def get_db():
	"""
	Description:
		Connect to our database
	"""
	conn = pymongo.MongoClient()
	db = conn['nbc_database']
	print('Succesfully Connected to Database')
	return db

def insert_in_db(json_path):
	"""
	Arguments:
		json_path - The path where our .json file is located
	Description:
		Pull up the .json file and for each entry in ['items'][i]['search_results']
	we insert it into the database.
	"""
	db = get_db()

	with open(json_path, 'r') as f:
		parsed = json.load(f)

	for i in range(len(parsed['items'])):
		print('Adding Search Result {0} Into The Database.'.format(i + 1))
		db.search_results.insert(parsed['items'][i], check_keys=False)