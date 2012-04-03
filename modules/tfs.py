#!/usr/bin/env python
"""
tfs.py - Phenny TFS Utilities
Perform commands on TFS for users
"""

import json


def tfs(phenny, input):
    f = open("modules/users.txt", 'r')
    users = json.load(f)

    for user in users:
        if user['nick'] == input.nick:
            machine = user['machine']

    if not machine:
        phenny.say("Couldn't find your machine, bro")
    else:
        phenny.say("Building on %s" % machine)

tfs.commands = ['tfs']
tfs.example = '.tfs main'
