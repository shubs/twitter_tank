#!/usr/bin/env python

import json
from datetime import datetime
from TwitterAPI import TwitterRestPager

import imp
twi = imp.load_source('twi', 'libs/twitter.py')
mongo = imp.load_source('mongo', 'libs/mongo.py')

api = twi.begin(1)
db = mongo.begin()

followers = twi.get_followers(api, 'shub_s')


# Only iterate through the first 200 statuses
for friend in followers
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