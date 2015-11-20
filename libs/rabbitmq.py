#!/usr/bin/env python
import pika

def enqueue(q_name, data):
	connection = pika.BlockingConnection(pika.ConnectionParameters(
	        host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue=q_name, durable=True)

	channel.basic_publish(exchange='',
	                      routing_key=q_name,
	                      body=data,
	                      properties=pika.BasicProperties(
	                         delivery_mode = 2, # make data persistent
	                      ))
	print " [x] Sent %r to %s" % (data, q_name)
	connection.close()