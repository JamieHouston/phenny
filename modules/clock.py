#!/usr/bin/env python
"""
clock.py - Phenny Clock Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import math, time, urllib, socket, struct, datetime
from decimal import Decimal as dec


def beats(phenny, input):
    """Shows the internet time in Swatch beats."""
    beats = ((time.time() + 3600) % 86400) / 86.4
    beats = int(math.floor(beats))
    phenny.say('@%03i' % beats)
beats.commands = ['beats']
beats.priority = 'low'


def divide(input, by):
    return (input / by), (input % by)


def yi(phenny, input):
    """Shows whether it is currently yi or not."""
    quadraels, remainder = divide(int(time.time()), 1753200)
    #raels = quadraels * 4
    extraraels, remainder = divide(remainder, 432000)
    if extraraels == 4:
        return phenny.say('Yes! PARTAI!')
    else:
        phenny.say('Not yet...')
yi.commands = ['yi']
yi.priority = 'low'


def tock(phenny, input):
    """Shows the time from the USNO's atomic clock."""
    u = urllib.urlopen('http://tycho.usno.navy.mil/cgi-bin/timer.pl')
    info = u.info()
    u.close()
    phenny.say('"' + info['Date'] + '" - tycho.usno.navy.mil')
tock.commands = ['tock']
tock.priority = 'high'


def npl(phenny, input):
    """Shows the time from NPL's SNTP server."""
    # for server in ('ntp1.npl.co.uk', 'ntp2.npl.co.uk'):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto('\x1b' + 47 * '\0', ('ntp1.npl.co.uk', 123))
    data, address = client.recvfrom(1024)
    if data:
        buf = struct.unpack('B' * 48, data)
        d = dec('0.0')
        for i in range(8):
            d += dec(buf[32 + i]) * dec(str(math.pow(2, (3 - i) * 8)))
        d -= dec(2208988800L)
        a, b = str(d).split('.')
        f = '%Y-%m-%d %H:%M:%S'
        result = datetime.datetime.fromtimestamp(d).strftime(f) + '.' + b[:6]
        phenny.say(result + ' - ntp1.npl.co.uk')
    else:
        phenny.say('No data received, sorry')
npl.commands = ['npl']
npl.priority = 'high'

if __name__ == '__main__':
    print __doc__.strip()
