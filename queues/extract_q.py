#!/usr/bin/env python
import pika
import sys
import tweepy
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('credentials.cfg')

consumer_key = parser.get('Twitter3', 'consumer_key')
consumer_secret = parser.get('Twitter3', 'consumer_secret')
access_token = parser.get('Twitter3', 'access_token')
access_token_secret = parser.get('Twitter3', 'access_token_secret')

print consumer_key

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


user = api.get_user('gsempe')


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='extract_q', durable=True)

for friend in user.followers_ids():
	message = str(friend)
	channel.basic_publish(exchange='',
	                      routing_key='extract_q',
	                      body=message,
	                      properties=pika.BasicProperties(
	                         delivery_mode = 2, # make message persistent
	                      ))
	print " [x] Sent %r" % (message,)
connection.close()