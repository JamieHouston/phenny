#!/usr/bin/env python
"""
tfs.py - Phenny TFS Utilities
Perform commands on TFS for users
"""

import json
import subprocess


def write_settings(phenny, input, new_vars={}, new_steps={}):
    config_vars = {
        "projectName": "corbisimages",
        "branch": "development/main",
        "workspaceName": "main",
        "buildConfig": "debug",
        "iisApplication": "localhost.corbisimages.corbis.pre",
        "publishFolder": "c:/publish/",
        "workspaceFolder": "c:\\workspaces\\<workspaceName>\\"
    }

    config_steps = {
        "CreateWorkspace": "false",
        "DeleteWorkspace": "false",
        "GetLatest": "false",
        "CleanBuild": "false",
        "Build": "false",
        "MapIIS": "false",
        "Publish": "false",
        "CreateBranch": "false"
    }

    config_vars.update(new_vars)
    config_steps.update(new_steps)

    filename = "{0}\\build.default.txt".format(phenny.bot.tfs[input.nick]['path'])

    f = open(filename, 'w')
    f.write('flag|ignore\n')

    for key, val in config_vars.items():
        f.write('var|{0}|{1}\n'.format(key, val))

    for key, val in config_steps.items():
        f.write('var|{0}|{1}\n'.format(key, val))

    f.close()


def run_scripts(phenny, input):
    try:
        file_command = "powershell %s\RunMe.ps1" % phenny.bot.tfs[input.nick]['path']
        subprocess.call(file_command)
        phenny.reply("Done")
    except Exception, e:
        phenny.say(("dude, it totally failed: {0}").format(e))


def tfs_local(phenny, input):
    if not phenny.bot.tfs[input.nick]['machine']:
        phenny.say(("Couldn't find your machine, {0}").format(input.nick))
    else:
        phenny.say(("Building on {0}").format(phenny.bot.tfs[input.nick]['machine']))
        write_settings(phenny, input)
        run_scripts(phenny, input)


def tfs_publish(phenny, input):
    f = open("modules/tfs.servers.txt", 'r')
    servers = json.load(f)

    for server in servers:
        if phenny.bot.tfs[input.nick]['options'] == server['environment']:
            server = server
            environment = server['environment']
            path = server['path']
            break

    if not environment:
        phenny.say(("Couldn't find your machine, {0}").format(input.nick))
    else:
        phenny.say(("Publishing to {0}").format(environment))
        write_settings(phenny, input, {"publishFolder": path, "buildConfig": environment}, {"Build": "true", "Publish": "true"})
        run_scripts(phenny, input)


def tfs_build(phenny, input):
    phenny.say("coming soon")


def tfs(phenny, input):
    """TFS Builder."""
    """build publish iis."""
    parameters = input.group(2)

    if not hasattr(phenny.bot, 'tfs'):
        phenny.bot.tfs = {}
        phenny.bot.tfs[input.nick] = {}

    if parameters:
        try:
            parameters = parameters.rsplit(' ')
            if len(parameters) > 1:
                command = parameters[0]
                options = parameters[1]
            else:
                command = parameters
                options = None
        except IndexError:
            phenny.reply("I can't work with that.\
                Try <command> <options> like \
                'publish sqa1' or 'build 12.2.02'")
            return
        phenny.bot.tfs[input.nick]['action'] = command
        phenny.bot.tfs[input.nick]['options'] = options
    else:
        command = None

    f = open("modules/users.txt", 'r')
    users = json.load(f)

    for user in users:
        if user['nick'] == input.nick:
            phenny.bot.tfs[input.nick]['machine'] = user['machine']
            phenny.bot.tfs[input.nick]['path'] = user['path']
            break

    if command == "build":
        if not options:
            phenny.reply("Which branch?")
        else:
            tfs_build(phenny, input)

    elif command == "publish":
        if not options:
            phenny.reply("Which environment?")
        else:
            tfs_publish(phenny, input)

    else:
        tfs_local(phenny, input)

tfs.commands = ['tfs']
tfs.example = '.tfs build <branch> or .tfs (to run default script)'
tfs.thread = True


# def tfs_request(phenny, input):
#     if not hasattr(phenny.bot, 'tfs'):
#         return

#     if phenny.bot.tfs[input.sender] and phenny.bot.tfs[input.sender]['action']:
#         phenny.bot.tfs[input.sender]['answer'] = input
#         action = phenny.bot.tfs[input.sender]['action']
#         tellee = input.nick

#         phenny.say(("I can {0} that for you, {1}").format(action, tellee))

#         phenny.bot.tfs[input.sender] = None

# tfs_request.rule = r'(.*)'
