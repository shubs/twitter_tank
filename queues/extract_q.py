#!/usr/bin/env python
import pika
import sys

import json
from datetime import datetime

import imp
twi = imp.load_source('twi', 'libs/twitter.py')
mongo = imp.load_source('mongo', 'libs/mongo.py')

api = twi.begin(1)
db = mongo.begin()

followers = twi.get_followers_ids(api, 'shub_s')

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='extract_q', durable=True)

followers = twi.get_followers_ids(api, 'gsempe')

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

for f in chunks(followers, 100):
	message = str(f)
	channel.basic_publish(exchange='',
	                      routing_key='extract_q',
	                      body=message,
	                      properties=pika.BasicProperties(
	                         delivery_mode = 2, # make message persistent
	                      ))
	print " [x] Sent %r" % (message,)
connection.close()