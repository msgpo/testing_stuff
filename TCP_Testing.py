import itertools
from subprocess import Popen, PIPE
import re
import sys

KEYVALUE_RE = re.compile(r'([^=]+)=(.*)')

def events(stream):
    """
    Read udev events from the stream, yielding them as dictionaries.
    """
    while True:
        event = dict(
            KEYVALUE_RE.match(line).groups()
            for line in itertools.takewhile(KEYVALUE_RE.match, stream)
        )
        if event:
            yield event

try:
    UDEVADM = ['/sbin/udevadm', 'monitor', '--udev', '--property']
    with Popen(UDEVADM, stdout=PIPE, encoding='UTF-8') as udevadm:
        for event in events(udevadm.stdout):
            if event['ACTION'] == 'add' and event.get('DRIVER') == 'usb-storage':
                print(event)
                break
except KeyboardInterrupt:
    sys.exit(1)