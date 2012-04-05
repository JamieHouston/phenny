#!/usr/bin/env python
"""
interactive.py - Phenny interactive module
Interact with people in the channel
"""

import random


def message_join(phenny, input):

    if input.nick == phenny.nick:
        back = ("Did ya miss me?", "I'm baaaaccckk", "What's up y'all!", "Anyone see the game last night?", "Me again.", "Howdy folks")
        phenny.say(random.choice(back))
    else:
        greetings = ("welcome ,%s", "what's up, %s", "hey everyone, %s is here!", "Look what the cat dragged in.", "Guess who's back!")
        phenny.say(random.choice(greetings) % input.nick)
message_join.event = 'JOIN'
message_join.rule = r'.*'


def thanks(phenny, input):
    welcome = ("You're welcome", "For what?", "No problem", "Why?", "Okay")
    phenny.say(random.choice(welcome))
thanks.rule = r'(?i)(thanks|thank you) $nickname[ \t]*$'


def good_night(phenny, input):
    night = ("So soon?", "Finally", "Later", "I guess we can't all put in 24 hours a day", "You'll be back")
    phenny.say(random.choice(night))
good_night.rule = r'(?i)(bye|good night|see ya) $nickname[ \t]*$'


def beer_me(phenny, input):
    beers = ("One cold one, coming up", "A little early, no?", "My pleasure", "Looks like Zak drank them all.", "I... hic... don't see any...")
    phenny.say(random.choice(beers))
beer_me.rule = r'(?i)(beer me) $nickname[ \t]*$'
