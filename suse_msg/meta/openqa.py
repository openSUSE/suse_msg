#!/usr/bin/python3

import re
from suse_msg.meta import BaseProcessor

class OpenQAProcessor(BaseProcessor):
    topic_regex = r"(?P<scope>[^.]+)\.openqa\.(?P<object>[^.]+)\.(?P<event>[^.]+)"

    def prepare(self):
        m = re.match(type(self).topic_regex, self.topic)
        self.scope = m.group('scope')
        self.object = m.group('object')
        self.event = m.group('event')

    def fmt(self, c):
        s = "openQA %s %s" % (self.object, self.event_past_perfect())

        if self.object == 'job':
            if self.event == 'done':
                s += " with result "
                s += self.colored_job_result(c)
            s += ": " + self.job_url()
        return s

    def colored_job_result(self, c):
        if 'result' not in self.msg:
            return 'n/a'
        color = {
            "failed": "lightred",
            "parallel_failed": "yellow",
            "softfailed": "lightyellow",
            "passed": "lightgreen",
            "obsoleted": "blue",
            "user_cancelled": "red",
            "incomplete": "red",
        }.get(self.msg['result'], None)
        return c(self.msg['result'], color)

    def event_past_perfect(self):
        return {
            "create": "created",
            "update": "updated",
            "delete": "deleted",
            "cancel": "canceled",
            "restart": "restarted",
            "duplicate": "duplicated",
            "done": "finished",
        }.get(self.event, '%sed' % self.event)
        
    def job_url(self):
        return self.base_url() + "t%i" % int(self.msg['id'])

    def base_url(self):
        if self.scope == 'suse':
            return 'https://openqa.suse.de/'
        elif self.scope == 'opensuse':
            return 'https://openqa.opensuse.org/'
