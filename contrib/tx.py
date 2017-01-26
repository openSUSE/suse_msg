#!/usr/bin/python3

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='kazhua.suse.de'))
channel = connection.channel()

channel.exchange_declare(exchange='pubsub', type='topic', passive=True, durable=True)

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='pubsub', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()
