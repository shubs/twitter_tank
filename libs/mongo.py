from pymongo import MongoClient

def begin():
	client = MongoClient()
	db = client.twitter
	return db

def add(db, info, payload):
	info['payload'] = payload
	result = db.users.insert_one(info)
	return result