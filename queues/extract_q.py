#!/usr/bin/env python
import pika
import sys
import imp
twi = imp.load_source('twi', 'libs/twitter.py')

api = twi.begin(1)

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