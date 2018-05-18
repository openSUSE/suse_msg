#!/usr/bin/python3

import pika
import json


# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.items() if k]
        
        return "%s\n\n" % "\n".join(lines)


def callback(ch, method, properties, body):
	try:
		jb = json.loads(body.decode('utf-8'))
		e = json.dumps({'topic': method.routing_key, 'body': jb})
		ev = ServerSentEvent(str(e))
		print(ev.encode())
	except ValueError:
		pass

print("Content-type: text/event-stream\r\n\r")

connection = pika.BlockingConnection(pika.URLParameters("amqp://opensuse:opensuse@localhost?heartbeat_interval=5"))
channel = connection.channel()
channel.exchange_declare(exchange='pubsub', exchange_type='topic', passive=True, durable=True)
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='pubsub', queue=queue_name, routing_key='#')
channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
