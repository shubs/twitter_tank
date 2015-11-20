#!/usr/bin/env python

import json
from datetime import datetime

import imp
twi = imp.load_source('twi', 'libs/twitter.py')
mongo = imp.load_source('mongo', 'libs/mongo.py')

api = twi.begin(1)
db = mongo.begin()

followers = twi.get_followers_ids(api, 'shub_s')

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

for f in chunks(followers, 100):
	r = api.request('users/lookup', {'user_id':f})
	print r.get_rest_quota()
	for e in r.json():
		payload = {
			'added on' : datetime.now(),
			'mute' : False,
			'following' : True,
			'step' : 0, 
			'score' : -1 #if -1 means never unfollow
		}
		result = mongo.add(db, e, payload)
		print result
# Only iterate through the first 200 statuses
# for friend in followers
#     # Process the friend here
# 	print friend.screen_name

# 	payload = {
# 		'added on' : datetime.now(),
# 		'mute' : False,
# 		'following' : False,
# 		'step' : 0, 
# 		'score' : 54 #if -1 means never unfollow
# 	}

# 	result = mongo.add(db, friend._json, payload)
# 	print result