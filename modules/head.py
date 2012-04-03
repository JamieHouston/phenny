#!/usr/bin/env python
"""
head.py - Phenny HTTP Metadata Utilities
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, httplib, time
import web


def head(phenny, input):
    """Provide HTTP HEAD information."""
    uri = input.group(2)
    uri = (uri or '').encode('utf-8')
    if ' ' in uri:
        uri, header = uri.rsplit(' ', 1)
    else:
        uri, header = uri, None

    if not uri and hasattr(phenny, 'last_seen_uri'):
        try:
            uri = phenny.last_seen_uri[input.sender]
        except KeyError:
            return phenny.say('?')

    if not uri.startswith('htt'):
        uri = 'http://' + uri
   # uri = uri.replace('#!', '?_escaped_fragment_=')

    try:
        info = web.head(uri)
    except IOError:
        return phenny.say("Can't connect to %s" % uri)
    except httplib.InvalidURL:
        return phenny.say("Not a valid URI, sorry.")

    if not isinstance(info, list):
        try:
            info = dict(info)
        except TypeError:
            return phenny.reply('Try .head http://example.org/ [optional header]')
        info['Status'] = '200'
    else:
        newInfo = dict(info[0])
        newInfo['Status'] = str(info[1])
        info = newInfo

    if header is None:
        data = []
        if 'Status' in info:
            data.append(info['Status'])
        if 'content-type' in info:
            data.append(info['content-type'].replace('; charset=', ', '))
        if 'last-modified' in info:
            modified = info['last-modified']
            modified = time.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z')
            data.append(time.strftime('%Y-%m-%d %H:%M:%S UTC', modified))
        if 'content-length' in info:
            data.append(info['content-length'] + ' bytes')
        phenny.reply(', '.join(data))
    else:
        headerlower = header.lower()
        if headerlower in info:
            phenny.say(header + ': ' + info.get(headerlower))
        else:
            msg = 'There was no %s header in the response.' % header
            phenny.say(msg)
head.commands = ['head']
head.example = '.head http://www.w3.org/'

r_title = re.compile(r'(?ims)<title[^>]*>(.*?)</title\s*>')
r_entity = re.compile(r'&[A-Za-z0-9#]+;')


def noteuri(phenny, input):
    uri = input.group(1).encode('utf-8')
    if not hasattr(phenny.bot, 'last_seen_uri'):
        phenny.bot.last_seen_uri = {}
    phenny.bot.last_seen_uri[input.sender] = uri
noteuri.rule = r'.*(http[s]?://[^<> "\x01]+)[,.]?'
noteuri.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
