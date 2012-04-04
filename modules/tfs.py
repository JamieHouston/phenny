#!/usr/bin/env python
"""
tfs.py - Phenny TFS Utilities
Perform commands on TFS for users
"""

import json
import subprocess


def tfs(phenny, input):
    """TFS Builder."""
    """build publish iis."""
    parameters = input.group(2)

    if not hasattr(phenny.bot, 'tfs'):
        phenny.bot.tfs = {}

    if ' ' in parameters:
        parameters = parameters.rsplit(' ')
        command = parameters[0]
    else:
        command = parameters

    phenny.bot.tfs[input.sender] = {}
    phenny.bot.tfs[input.sender]['action'] = command

    if command == "build":
        phenny.reply("Which branch?")

    elif command == "publish":
        phenny.reply("Which environment?")

    else:
        f = open("modules/users.txt", 'r')
        users = json.load(f)

        for user in users:
            if user['nick'] == input.nick:
                machine = user['machine']
                path = user['path']
                break

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
tfs.example = '.tfs build <branch> or .tfs (to run default script)'
tfs.thread = True


def tfs_request(phenny, input):
    if not hasattr(phenny.bot, 'tfs'):
        return

    if phenny.bot.tfs[input.sender] and phenny.bot.tfs[input.sender]['action']:
        phenny.bot.tfs[input.sender]['answer'] = input
        action = phenny.bot.tfs[input.sender]['action']
        tellee = input.nick

        phenny.say('I can %s that for you %s' % (action, tellee))

        phenny.bot.tfs[input.sender] = None

tfs_request.rule = r'(.*)'
