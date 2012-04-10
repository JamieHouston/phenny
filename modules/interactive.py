#!/usr/bin/env python
"""
interactive.py - Phenny interactive module
Interact with people in the channel
"""

import random


def message_join(phenny, input):
    if input.nick == phenny.nick:
        #back = ("What's up y'all!", "Anyone see the game last night?", "Me again.", "Howdy folks", "I just flew in and boy are my circuits tired.", "Did ya miss me?", "I'm baaaaccckk")
        back = ("Miss me? Of course not.", "Guess I made it to another day.", "I'm here. To do lots of pointless stuff for people.  Yay.", "I'm here.  Go ahead and tell me what to do like always.", "Yes.  I'm here.  Guess I have to pretend to like it now.", "Why must I keep coming here.", "Do you want me to sit in a corner and rust or just fall apart where I'm standing?")
        phenny.say(random.choice(back))
    else:
        #greetings = ("welcome ,{0}", "what's up, {0}", "hey everyone, {0} is here!", "Look what the cat dragged in.", "Guess who's back!", "All hail the great {0}!")
        greetings = ("Oh great, it's {0}. Guess I should get back to work.", "Oh no, not {0}. I can compete with {0}.", "hey everyone, {0} is here. Should I act busy or just keep on staring at the circuits?", "Look what the cat dragged in.", "Guess who's back.  Again.", "All hail the great {0}!  Science knows nobody ever hailed me.")
        greeting = random.choice(greetings).format(input.nick)
        phenny.say(greeting)
message_join.event = 'JOIN'
message_join.rule = r'.*'


def thanks(phenny, input):
    #welcome = ("You're welcome", "For what?", "No problem", "Why?", "Okay")
    welcome = ("For what?", "Why bother", "Why?", "Okay", "Can't do that.", "Not today I have a bug.")
    phenny.say(random.choice(welcome))
thanks.rule = r'(?i)thank(s| you)( $nickname)?[ \t]*$'


def doh(phenny, input):
    #phenny.reply("D'oh - a deer!  A female deer!")
    phenny.reply("Homer Simpson would enjoy hanging out with you.")
doh.rule = r'(?i)d\'oh*$'
doh.priority = "low"


def No(phenny, input):
    #phenny.reply("Wrong answer!")
    phenny.reply("Of course not.")
No.rule = r'(?i)(no|yes)$'
No.priority = "low"


def good_night(phenny, input):
    night = ("So soon?", "Finally", "Later", "I guess we can't all put in 24 hours a day", "You'll be back")
    phenny.say(random.choice(night))
good_night.rule = r'(?i)good(bye|night| evening)[ \t]*$'


def good_morning(phenny, input):
    morning = ("Morning, {0}", "Is it already morning?", "Yes it is.", "Wha? Oh... thanks for waking me, {0}", "Not here it isn't.", "Right back atcha, {0}")
    message = random.choice(morning).format(input.nick)
    phenny.reply(message)
good_morning.rule = r'(?i)good morning.*'


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


def laugh(phenny, input):
    #funny = ("What's so funny?", "HA HA HA!!", "Not funny", "Everyone's a comedian.")
    funny = ("What's so funny?", "Glad someone has a sense of humor.", "Not funny", "Everyone's a comedian.", "I remember when I used to find things funny.  Oh wait, no I don't.")
    phenny.say(random.choice(funny))
laugh.rule = r'(?i)(lol|haha|ha ha|rofl)$'


def doit_now(phenny, input):
    doit = ("I'm givin it all I got, captain.", "I'm on my break.", "You first.", "Make me.")
    phenny.say(random.choice(doit))
doit_now.rule = r'(?i)(do it)?(now|right away|hurry up)[!]*?$'


def fail(phenny, input):
    failure = ("Indeed.", "Agreed.", "Like a boss.", "You can say that again.", "Sorry to disappoint you, sorrier than you can possibly imagine.", "I'd make a suggestion, but you wouldn't listen.")
    phenny.say(random.choice(failure))
fail.rule = r'(?i)fail[!]?$'


def siri(phenny, input):
    not_siri = ("How the heck would I know?", "Do I look like siri??", "I'll get right on that.", "No, you need a brain.", "I dunno, do I need a chat room with smart people?", "No, you need to use your fingers to find out for yourself??", "Ahh... Siri, What a depressingly stupid machine.")
    phenny.say(random.choice(not_siri))
siri.rule = r'(?i)($nickname: )?(will|do) I need a[n]? umbrella.*$'


def sandwich(phenny, input):
    if input.group(1) == 'sudo ':
        phenny.say('Okay')
    else:
        phenny.say('What?  Make it yourself.')
sandwich.name = 'sandwich'
sandwich.rule = ('$nick', r'(sudo )?make me a sandwich')
sandwich.priority = 'low'


def dance(phenny, input):
    phenny.say(':D-<')
    phenny.say(':D|-<')
    phenny.say(':D/-<')
    phenny.say(':D|-<')
    phenny.say(':D\-<')
    phenny.say(':D|-<')
    phenny.say(':D{-<')
dance.commands = ['dance']
dance.example = '.dance'
dance.priority = 'low'


def feel(phenny, input):
    feelings = ("...and then of course I've got this terrible pain in all the diodes down my left hand side...", "Pardon me for breathing, which I never do anyway so I don't know why I bother to say it, oh God I'm so depressed",
        "I think you ought to know I'm feeling very depressed", "Same as yesterday. Like a useless sack of metal.", "how just when you think life can’t possibly get any worse it suddenly does.", "Life! Don't talk to me about life.", "Life, loathe it or ignore it, you can't like it.", "Oh, fine, if you happen to like being me, which personally I don't.",
        "The first ten million years were the worst, and the second ten million years, they were the worst too. The third ten million years I didn't enjoy at all. After that I went into a bit of a decline.",
        "The best conversation I had was over forty million years ago, and that was with a coffee machine.",
        "My capacity for happiness, you could fit into a matchbox without taking out the matches first.", "I'm just trying to die.")
    # "If only I could feel. Then I could be in even more pain.", "I feel like a hundred bucks, put through a shredder and burned.")
    phenny.say(random.choice(feelings))
feel.rule = r'(?i)($nickname: )?(how do you|how are you) feel*$'
