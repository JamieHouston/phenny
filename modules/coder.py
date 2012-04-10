#!/usr/bin/env python
"""
web.py - Web Facilities
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import web


def commit_message(phenny, input):
    result = web.get("http://whatthecommit.com/index.txt")
    phenny.reply(result)
commit_message.commands = ['commit']
commit_message.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
