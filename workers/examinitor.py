#!/usr/bin/env python
import pika
import time
from ConfigParser import SafeConfigParser
from tinydb import TinyDB, where
import tweepy

db = TinyDB('data/database.json')

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

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='examine_q', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(1)
    #lookup information
    #add to db..
    #add to DB

    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='examine_q')

channel.start_consuming()