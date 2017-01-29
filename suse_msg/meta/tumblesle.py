import re
from suse_msg.meta import BaseProcessor


# limit is 512 including all characters, just split it somewhere
MSG_LIMIT = 400


class TumbleSLEProcessor(BaseProcessor):
    topic_regex = r"(?P<scope>[^.]+)\.tumblesle\.(?P<event>[^.]+)"

    def prepare(self):
        m = re.match(type(self).topic_regex, self.topic)
        self.scope = m.group('scope')
        self.event = m.group('event')

    def fmt(self, c):
        result = self.colored_result(c)
        msg = ', '.join('%s: %s' % (k, v) for k, v in self.msg.items())
        # prevent irc.client.MessageTooLong
        if len(msg) > MSG_LIMIT:
            msg = msg[0:MSG_LIMIT] + '…'
        s = "tumbleSLE %s: %s" % (result, msg)
        return s

    def colored_result(self, c):
        color = {
            "regression": "lightred",
            "release": "lightgreen",
        }.get(self.event, None)
        return c(self.event, color)
