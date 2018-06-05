import logging
import re
from collections import deque
from suse_msg.meta import BaseProcessor


logging.basicConfig(level=logging.INFO)


MSG_LIMIT = 220

# limit of how many times a truncated message has to show up the same before we repeat it
SEEN_LIMIT = 1
SEEN = deque(maxlen=SEEN_LIMIT)

def truncate(s):
    if len(s) > MSG_LIMIT:
        s = s[0:MSG_LIMIT] + '…'
    return s


def comma_entries(l):
    if type(l) is not list:
        return l
    return ', '.join(l)


class TTMProcessor(BaseProcessor):
    topic_regex = r"(?P<scope>[^.]+)\.ttm\.(?P<object>[^.]+)\.(?P<event>[^.]+)"

    def prepare(self):
        m = re.match(type(self).topic_regex, self.topic)
        self.scope = m.group('scope')
        self.object = m.group('object')
        self.event = m.group('event')

    def fmt(self, c):
        if self.object != 'build':
            # only build object output is implemented
            return ''

        s = "TTM: %s build %s " % (self.msg['project'], self.msg['build'])
        s += self.colored_result(c)

        if self.event != 'pass':
            if len(self.msg['failed_jobs']['relevant']) == 0:
                s += " - not unknown fails" + ' yet!' if self.event == 'inprogress' else '!'
            else:
                s += " - unknown fails: "
                s += truncate(' '.join(["%st%i" % (self.base_url(), buildid) for buildid in self.msg['failed_jobs']['relevant']]))

        if s in SEEN:
            logging.info("Ignoring already seen message '%s'" % s)
            return ''
        else:
            logging.info("not found s in self.seen. self.seen: %s" % SEEN)
        SEEN.append(s)
        return s

    def colored_result(self, c):
        color = {
            "fail": "lightred",
            "pass": "lightgreen",
            "inprogress": "yellow",
        }.get(self.event, None)
        return c(self.event, color)

    def base_url(self):
        if self.scope == 'suse':
            return 'https://openqa.suse.de/'
        elif self.scope == 'opensuse':
            return 'https://openqa.opensuse.org/'
