#!/usr/bin/env python
"""
tfs.py - Phenny TFS Utilities
Perform commands on TFS for users
"""

import json
import subprocess
import sys
import random
import tools


class Tfs_Handler(object):
    def __init__(self, settings, phenny):
        self.settings = settings
        self.phenny = phenny

    def get_branch(self, branch):
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

    def write_settings(self, new_vars={}, new_steps={}):
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

        filename = "{0}\\build.default.txt".format(self.settings.script_path)

        f = open(filename, 'r')
        for line in f:
            line = line.strip()
            if line.startswith("var|"):
                option = line.split("|")
                config_vars[option[1]] = option[2]
        f.close()

        config_vars.update(new_vars)
        config_steps.update(new_steps)

        config_vars["branch"] = self.get_branch(config_vars["branch"])

        f = open(filename, 'w')
        f.write('flag|ignore\n')

        for key, val in config_vars.items():
            f.write('var|{0}|{1}\n'.format(key, val))

        for key, val in config_steps.items():
            f.write('step|{0}|{1}\n'.format(key, val))

        f.close()

    def run(self, new_vars, new_steps):
        if not self.settings.machine:
            self.phenny.say("Couldn't find your machine")
        else:
            self.write_settings(new_vars, new_steps)
            try:
                #if self.settings.command == "publish":
                #    file_command = "powershell.exe C:\\dev\\scripts\\CorbisBuilder5000X\\RunMe-Remote.ps1"
                #else:
                #    file_command = "C:\\Windows\\SysNative\\WindowsPowerShell\\v1.0\\powershell.exe %s\RunMe.ps1" % self.settings.script_path
                #file_command = "powershell %s\RunMe.ps1" % self.settings.script_path
                file_command = "C:\\Windows\\SysNative\\WindowsPowerShell\\v1.0\\powershell.exe %s\RunMe.ps1" % self.settings.script_path
                subprocess.call(file_command)
            except Exception, e:
                self.phenny.say(("dude, it totally failed: {0}").format(e))

            finished = ("As they say in Coming to America, your royal project is clean.", "Ding fries are done.", "Back to work, I'm finished.", "All done, your majesty.", "Anything else you need?",
                "I've finished your stupid work.", "Done.  But I'm sure you have more for me to do.")
            self.phenny.reply(random.choice(finished))

    def update_config(self, path, old_environment, new_environment):
        from xml.dom.minidom import parse

        to_replace = (
            "restfulEndpoints",
            "searchSettings",
            "clientEndpoints",
        )

        full_path = "{0}\{1}".format(path, "web.config")
        web_config = parse(full_path)

        for endpoint in to_replace:
            setting = web_config.getElementsByTagName(endpoint)[0]
            setting.setAttribute("configSource",
                setting.getAttribute("configSource").replace(old_environment, new_environment)
            )

        f = open(full_path)
        try:
            f.write(web_config.toprettyxml(index="  "))
        finally:
            f.close()

    def publish(self):
        f = open("modules/tfs.servers.txt", 'r')
        #self.settings.script_path = self.settings.machine = "\\\\dl00testapi01\\CorbisBuilder5000X"

        servers = json.load(f)

        for server in servers:
            if self.settings.environment == server['environment']:
                print >> sys.stderr, "Found server: {0}".format(self.settings.environment)
                server = server
                environment = server['environment']
                self.settings.project_path = server['path']
                break

        self.run({"publishFolder": self.settings.project_path, "buildConfig": environment, "branch": self.settings.branch, "workspaceName": self.settings.branch}, {"Build": "true", "Publish": "true", "DeleteWorkspace": "true", "CreateWorkspace": "true", "GetLatest": "true"})
        if hasattr(self.settings, 'transform'):
            self.update_config(self.settings.project_path, environment, environment.replace(environment, self.settings.transform))

    def build(self):
        branch = self.settings.branch
        self.run({"buildConfig": "debug", "branch": branch, "workspaceName": branch}, {"CreateWorkspace": "true", "Build": "true", "GetLatest": "true", "MapIIS": "true"})

    def mapiis(self):
        branch = self.settings.branch
        self.run({"branch": branch, "workspaceName": branch}, {"MapIIS": "true"})

    def create_branch(self):
        branch = self.settings.branch
        self.run({"branch": branch}, {"createBranch": "true"})


def tfs(phenny, input):
    """ TFS Builder.
        build publish iismap
        <command> <branch> [on] <target> <config>
        publish 12.2.01 on dev1 with sqa1
            will publish 12.2.01 release on dev1, replacing dev1 endpoints with sqa1
        build mybranch
            will build mybranch on local box
        mapiis 12.2.01 on local
            will change local iis settings to map to 12.2.01 branch
    """
    print >> sys.stderr, input.group

    parameters = []
    for item in input.group(0).split(' '):
        key = item.strip()
        if key not in ['on', 'to', 'from', 'with', 'using'] and len(key) > 0:
            parameters.append(key)

    command = parameters[0]

    doit = ("I'll get right on that {0}, sir.", "Here I am, brain the size of a planet and they ask me to {0}. Call that job satisfaction? 'Cos I don't.", "I guess I'll start the {0}",
        "I would like to say that it is a very great pleasure, honour and privilege for me to {0}, but I can't because my lying circuits are all out of commission.",
        "{0}, eh? It won't work.")
    phenny.say(random.choice(doit).format(command))

    print >> sys.stderr, "Running TFS command: {0}".format(command)

    # if parameters:
    #     try:
    #         parameters = parameters.rsplit(' ')
    #         if len(parameters) > 1:
    #             command = parameters[0]
    #             options = parameters[1]
    #         else:
    #             command = parameters
    #             options = None
    #     except IndexError:
    #         phenny.reply("I can't work with that.\
    #             Try <command> <options> like \
    #             'publish sqa1' or 'build 12.2.02'")
    #         return
    #     #phenny.bot.tfs[input.nick]['action'] = command
    #     #phenny.bot.tfs[input.nick]['options'] = options
    # else:
    #     command = None

    # Prime the pump
    settings = tools.Dynamo()
    settings.command = command

    if not hasattr(phenny.bot, 'tfs'):
        phenny.bot.tfs = {}
        phenny.bot.tfs[input.nick] = {}

    f = open("modules/users.txt", 'r')
    users = json.load(f)

    for user in users:
        if user['nick'] == input.nick:
            settings.machine = user['machine']
            settings.script_path = user['path']
            break
    try:
        settings.branch = parameters[1]
        if command == "publish":
            settings.environment = parameters[2]
            print >> sys.stderr, "Publish environment: {0}".format(settings.environment)
            if len(parameters) == 4:
                settings.transform = parameters[3]
    except Exception, e:
        phenny.say("Zing!: {0}".format(e))
        return

    handler = Tfs_Handler(settings, phenny)
    tfs_command = command.replace(' ', '_')
    if hasattr(handler, tfs_command):
        runner = getattr(handler, tfs_command)
        runner()

tfs.rule = r'(?i)(build|publish|mapiis) ([\d\w\.\-]*)(?: | on | to )?([\d\w\.])+(?: | with | using )?([\d\w\.]*)$'
#tfs.commands = ['tfs']
tfs.example = 'build 12.2.01 or publish sqa1 on dev1'
tfs.thread = True


# def tfs_request(phenny, input):
#     if not hasattr(phenny.bot, 'tfs'):
#         return

#     tellee = input.nick

#     if tellee in phenny.bot.tfs and 'question' in phenny.bot.tfs[tellee]:
#         question = phenny.bot.tfs[tellee]['question']
#         phenny.bot.tfs[tellee][question] = input
#         action = phenny.bot.tfs[tellee]['action']

#         del phenny.bot.tfs[tellee]['question']

#         phenny.say(("I can {0} that for you, {1}").format(action, tellee))

#         if action == "build":
#             tfs_build(phenny, input)
#         elif action == "publish":
#             tfs_publish(phenny, input)
#         elif action == "mapiis":
#             tfs_mapiis(phenny, input)

# tfs_request.rule = r'(.*)'
