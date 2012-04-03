#!/usr/bin/env python
"""
tfs.py - Phenny TFS Utilities
Perform commands on TFS for users
"""

import json
import subprocess


def tfs(phenny, input):
    """TFS Builder."""
    if "build" in input.group(2):
        phenny.reply("Wouldn't that be cool.")
    elif "publish" in input.group(2):
        phenny.say("initiating missle launch")
    else:
        f = open("modules/users.txt", 'r')
        users = json.load(f)

        for user in users:
            if user['nick'] == input.nick:
                machine = user['machine']
                path = user['path']

        if not machine:
            phenny.say("Couldn't find your machine, bro")
        else:
            phenny.say("Building on %s" % machine)
            try:
                file_command = "powershell %s\RunMe.ps1" % path
                subprocess.call(file_command)
                phenny.reply("Done")
            except Exception, e:
                phenny.say("dude, it totally failed: %s" % e)


tfs.commands = ['tfs']
tfs.example = '.tfs main'
tfs.thread = False
