#!/usr/bin/env python
"""
interactive.py - Phenny interactive module
Interact with people in the channel
"""

import random


def message_join(phenny, input):

    if input.nick == "CIBot2":
        back = ("Did ya miss me?", "I'm baaaaccckk", "What's up y'all!", "Anyone see the game last night?", "Me again.", "Howdy folks")
        phenny.say(random.choice(back))
    else:
        phenny.say("welcome, %s!" % input.nick)
message_join.event = 'JOIN'
message_join.rule = r'.*'


def thanks(phenny, input):
    welcome = ("You're welcome", "For what?", "No problem", "Why?", "Okay")
    phenny.say(random.choice(welcome))
thanks.rule = r'(?i)(thanks|thank you) $nickname[ \t]*$'


def beer_me(phenny, input):
    beers = ("One cold one, coming up", "A little early, no?", "My pleasure", "Looks like Zak drank them all.", "I... hic... don't see any...")
    phenny.say(random.choice(beers))
beer_me.rule = r'(?i)(beer me) $nickname[ \t]*$'
