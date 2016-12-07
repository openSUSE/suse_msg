#!/usr/bin/python3

import re

class Router(object):
    def __init__(self, routing_table):
        self.routing_table = {}
        self.channels = set()
        for key, channels in routing_table.items():
            self.channels.update(channels)
            rkey = key.replace('.', '\.').replace('*', '[^.]*').replace('#', '.*')
            self.routing_table[re.compile(rkey)] = channels

    def topic_channels(self, topic):
        destination_channels = set()
        for rkey, channels in self.routing_table.items():
            if rkey.match(topic):
                destination_channels.update(channels)
        return destination_channels
