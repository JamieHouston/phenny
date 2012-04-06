#!/usr/bin/env python
"""
tfs.py - Phenny TFS Utilities
Perform commands on TFS for users
"""

import json
import subprocess
import sys


def get_branch(branch):
    """
    Try and guess the branch
    Only works for CorbisImages solution...
    """
    root = ""
    if "/" in branch:
        return branch
    if branch == "main":
        root = "development"
    elif "." in branch:
        root = "releases"
    else:
        root = "features"

    return "{0}/{1}".format(root, branch)


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

    config_vars["branch"] = get_branch(config_vars["branch"])

    filename = "{0}\\build.default.txt".format(phenny.bot.tfs[input.nick]['path'])

    f = open(filename, 'w')
    f.write('flag|ignore\n')

    for key, val in config_vars.items():
        f.write('var|{0}|{1}\n'.format(key, val))

    for key, val in config_steps.items():
        f.write('step|{0}|{1}\n'.format(key, val))

    f.close()


def run_scripts(phenny, input):
    try:
        file_command = "C:\\Windows\\SysNative\\WindowsPowerShell\\v1.0\\powershell.exe %s\RunMe.ps1" % phenny.bot.tfs[input.nick]['path']
        subprocess.call(file_command)
    except Exception, e:
        phenny.say(("dude, it totally failed: {0}").format(e))


def tfs_handler(phenny, input, new_vars, new_steps):
    if not phenny.bot.tfs[input.nick]['machine']:
        phenny.say(("Couldn't find your machine, {0}").format(input.nick))
    else:
        phenny.say(("Starting on {0}").format(phenny.bot.tfs[input.nick]['machine']))
        write_settings(phenny, input, new_vars, new_steps)
        run_scripts(phenny, input)
        phenny.reply("Back to work, I'm done.")


def tfs_publish(phenny, input):
    f = open("modules/tfs.servers.txt", 'r')
    servers = json.load(f)

    for server in servers:
        if phenny.bot.tfs[input.nick]['options'] == server['environment']:
            server = server
            environment = server['environment']
            path = server['path']
            break

    tfs_handler(phenny, input, {"publishFolder": path, "buildConfig": environment}, {"Build": "true", "Publish": "true"})


def tfs_build(phenny, input):
    branch = phenny.bot.tfs[input.nick]['branch']
    tfs_handler(phenny, input, {"branch": branch, "workspaceName": branch}, {"CreateWorkspace": "true", "Build": "true", "GetLatest": "true", "MapIIS": "true"})


def tfs_mapiis(phenny, input):
    branch = phenny.bot.tfs[input.nick]['branch']
    tfs_handler(phenny, input, {"branch": branch, "workspaceName": branch}, {"MapIIS": "true"})


def tfs(phenny, input):
    """TFS Builder."""
    """build publish iis."""
    print >> sys.stderr, "running tfs"
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
            phenny.bot.tfs[input.nick]["question"] = "branch"
        else:
            tfs_build(phenny, input)

    elif command == "publish":
        if not options:
            phenny.reply("Which environment?")
            phenny.bot.tfs[input.nick]["question"] = "environment"
        else:
            phenny.bot.tfs[input.nick]['branch'] = options
            tfs_publish(phenny, input)
    elif command == "mapiis":
        if not options:
            phenny.reply("Which branch?")
            phenny.bot.tfs[input.nick]["question"] = "branch"
        else:
            phenny.bot.tfs[input.nick]['branch'] = options
            tfs_mapiis(phenny, input)
    else:
        phenny.reply("I have no idea what you want me to do")

tfs.commands = ['tfs']
tfs.example = '.tfs build <branch> or .tfs publish <environment>'
tfs.thread = True


def tfs_request(phenny, input):
    if not hasattr(phenny.bot, 'tfs'):
        return

    tellee = input.nick

    if tellee in phenny.bot.tfs and 'question' in phenny.bot.tfs[tellee]:
        question = phenny.bot.tfs[tellee]['question']
        phenny.bot.tfs[tellee][question] = input
        action = phenny.bot.tfs[tellee]['action']

        del phenny.bot.tfs[tellee]['question']

        phenny.say(("I can {0} that for you, {1}").format(action, tellee))

        if action == "build":
            tfs_build(phenny, input)
        elif action == "publish":
            tfs_publish(phenny, input)
        elif action == "mapiis":
            tfs_mapiis(phenny, input)

tfs_request.rule = r'(.*)'
