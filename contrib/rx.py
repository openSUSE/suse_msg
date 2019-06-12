#!/usr/bin/env python

import configargparse
import os.path
import pika
import sys


DEFAULTS = {
    'CONFIG_PATH': os.path.expanduser('~') + '/.config/amqp_xxrc',
    'CONFIG_USAGE': """
You are missing configuration file with the proper format.
Example:
[global]
host = rabbit.opensuse.org
user = opensuse
password = opensuse
""",
}


def parse_args():
    parser = configargparse.ArgParser(formatter_class=configargparse.ArgumentDefaultsHelpFormatter, default_config_files=[DEFAULTS['CONFIG_PATH']])
    parser.add('-H', '--host', help="The AMQP host to connect to", default = 'rabbit.opensuse.org')
    parser.add('--user', default="opensuse",
                        help="Username for the AMQP host")
    parser.add('--password', default="opensuse",
                        help="Password for the AMQP host")
    parser.add('--binding-keys', default="#",
                        help="AMQP binding keys, e.g. '#' to collect all or 'opensuse.obs.#' for all OBS events")
    parser.add('--amqp-options', default="heartbeat_interval=5",
                        help="AMQP options as query string, e.g. option1=X&option2=Y")
    parser.add('keys', help="AMQP routing keys", nargs='*')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    connection = pika.BlockingConnection(pika.URLParameters("amqps://%s:%s@%s?%s" % (args.user, args.password, args.host, args.amqp_options)))
    channel = connection.channel()
    channel.exchange_declare(exchange='pubsub', exchange_type='topic', passive=True, durable=True)
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    binding_keys = args.keys if args.keys else args.binding_keys
    for binding_key in binding_keys:
        channel.queue_bind(exchange='pubsub',
                           queue=queue_name,
                           routing_key=binding_key)
    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    main()
