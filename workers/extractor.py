#!/usr/bin/env python
import pika
import time


import json
from datetime import datetime

import imp
twi = imp.load_source('twi', 'libs/twitter.py')
mongo = imp.load_source('mongo', 'libs/mongo.py')

api = twi.begin(4)
db = mongo.begin()


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='extract_q', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
	print " [x] Received %r" % (body,)
	r = api.request('users/lookup', {'user_id':body})
	print r.get_rest_quota()
	for e in r.json():
		payload = {
			'added on' : datetime.now(),
			'mute' : False,
			'following' : False,
			'step' : 0, 
			'score' : 0 #if -1 means never unfollow
		}
		result = mongo.add(db, e, payload)
		print result

	print " [x] Done"
	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='extract_q')

channel.start_consuming()