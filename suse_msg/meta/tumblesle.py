import re
from suse_msg.meta import BaseProcessor


# limit is 512 including all characters, just split it somewhere
MSG_LIMIT = 400


def truncate(s):
    if len(s) > MSG_LIMIT:
        s = s[0:MSG_LIMIT] + '…'
    return s


def comma_entries(l):
    if type(l) is not list:
        return l
    return ', '.join(l)


class TumbleSLEProcessor(BaseProcessor):
    topic_regex = r"(?P<scope>[^.]+)\.tumblesle\.(?P<event>[^.]+)"

    def prepare(self):
        m = re.match(type(self).topic_regex, self.topic)
        self.scope = m.group('scope')
        self.event = m.group('event')

    def fmt(self, c):
        result = self.colored_result(c)
        # prevent irc.client.MessageTooLong
        msg = ', '.join('%s: %s' % (k, truncate(comma_entries(v))) for k, v in self.msg.items())
        s = "tumbleSLE %s: %s" % (result, msg)
        return s

    def colored_result(self, c):
        color = {
            "regression": "lightred",
            "release": "lightgreen",
        }.get(self.event, None)
        return c(self.event, color)
