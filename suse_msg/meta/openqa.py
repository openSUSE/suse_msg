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
        elif self.object == 'comment':
            if self.event == 'create':
                if self.is_group_event():
                    s += " on job group "
                if self.is_job_event():
                    s += " on job "
                s += "by %(user)s" % self.msg
                s += ": " + self.comment_url()
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

    def comment_url(self):
        if self.is_group_event():
            path = "group_overview/%i" % int(self.msg['group_id'])
        elif self.is_job_event():
            path = "t%i" % int(self.msg['job_id'])
        return "%s%s#comment-%i" % (self.base_url(), path, int(self.msg['id']))

    def is_group_event(self):
        return bool(self.msg.get('group_id'))

    def is_job_event(self):
        return bool(self.msg.get('job_id'))

    def base_url(self):
        if self.scope == 'suse':
            return 'https://openqa.suse.de/'
        elif self.scope == 'opensuse':
            return 'https://openqa.opensuse.org/'
