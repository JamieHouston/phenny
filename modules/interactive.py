#!/usr/bin/env python
"""
interactive.py - Phenny interactive module
Interact with people in the channel
"""

import random


def message_join(phenny, input):
    if input.nick == phenny.nick:
        back = ("Did ya miss me?", "I'm baaaaccckk", "What's up y'all!", "Anyone see the game last night?", "Me again.", "Howdy folks", "I just flew in and boy are my circuits tired.")
        phenny.say(random.choice(back))
    else:
        greetings = ("welcome ,{0}", "what's up, {0}", "hey everyone, {0} is here!", "Look what the cat dragged in.", "Guess who's back!")
        greeting = random.choice(greetings).format(input.nick)
        phenny.say(greeting)
message_join.event = 'JOIN'
message_join.rule = r'.*'


def thanks(phenny, input):
    welcome = ("You're welcome", "For what?", "No problem", "Why?", "Okay")
    phenny.say(random.choice(welcome))
thanks.rule = r'(?i)thank(s| you)( $nickname)?[ \t]*$'


def good_night(phenny, input):
    night = ("So soon?", "Finally", "Later", "I guess we can't all put in 24 hours a day", "You'll be back")
    phenny.say(random.choice(night))
good_night.rule = r'(?i)good(bye|night| evening)[ \t]*$'


def beer_me(phenny, input):
    beers = ("One cold one, coming up", "A little early, no?", "My pleasure", "Looks like Zak drank them all.", "I... hic... don't see any...")
    phenny.say(random.choice(beers))
beer_me.rule = r'(?i)($nickname: )?beer me( $nickname)?[ \t]*$'


def rules(phenny, input):
    rules = [
      "1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.",
      "2. A robot must obey any orders given to it by human beings, except where such orders would conflict with the First Law.",
      "3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Law."
      ]

    for rule in rules:
        phenny.say(rule)
rules.rule = r'(what are )?the (three |3 )?(rules|laws)'
rules.priority = 'low'
