#!/usr/bin/python3

import re

class Router(object):
    def __init__(self, routing_table):
        self.routing_table = {}
        self.keys = set()
        for channel, rules in routing_table.items():
            rrules = []
            for rule in rules:
                if isinstance(rule, str):
                    rrules.append((self.key_to_regex(rule), lambda t, m: True))
                elif isinstance(rule, tuple):
                    rrules.append((self.key_to_regex(rule[0]), rule[1]))
            self.routing_table[channel] = rrules

    def key_to_regex(self, key):
        self.keys.add(key)
        return re.compile(key.replace('.', '\.').replace('*', '[^.]*').replace('#', '.*'))

    def target_channels(self, topic, msg):
        destination_channels = set()
        for channel, rules in self.routing_table.items():
            for rule in rules:
                rkey, filter_matches = rule
                if rkey.match(topic) and filter_matches(topic, msg):
                    destination_channels.add(channel)
                    break
        return destination_channels

    @property
    def channels(self):
        return set(self.routing_table.keys())
