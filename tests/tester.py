#!/usr/bin/env python

import json
from datetime import datetime
import tweepy

import imp
twi = imp.load_source('twi', 'libs/twitter.py')
mongo = imp.load_source('mongo', 'libs/mongo.py')

api = twi.begin(1)
db = mongo.begin()

user = api.get_user('shub_s')

print user.screen_name
print user.followers_count


# Only iterate through the first 200 statuses
for friend in tweepy.Cursor(api.friends).items():
    # Process the friend here
	print friend.screen_name

	payload = {
		'added on' : datetime.now(),
		'mute' : False,
		'following' : False,
		'step' : 0, 
		'score' : 54 #if -1 means never unfollow
	}

	result = mongo.add(db, friend._json, payload)
	print result