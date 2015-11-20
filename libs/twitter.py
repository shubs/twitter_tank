from ConfigParser import SafeConfigParser
from TwitterAPI import TwitterAPI
import time

def begin(num):
	parser = SafeConfigParser()
	parser.read('credentials.cfg')

	key_name = 'Twitter'+str(num)

	consumer_key = parser.get(key_name, 'consumer_key')
	consumer_secret = parser.get(key_name, 'consumer_secret')
	access_token = parser.get(key_name, 'access_token')
	access_token_secret = parser.get(key_name, 'access_token_secret')

	print "Twitter init with key : "+ str(num) + "\t key : " + consumer_key

	
	api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
	return api

def get_followers(api, name):

	r = api.request('followers/ids', {'screen_name':'gsempe'})
	cursor = r.json()['next_cursor']
	followers = r.json()['ids']

	while cursor != 0:		
		#time.sleep(1)
		r = api.request('followers/ids', {'screen_name':'gsempe', 'cursor':cursor})
		cursor = r.json()['next_cursor']
		followers = followers + r.json()['ids']

	return followers