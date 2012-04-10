#!/usr/bin/env python
"""
hubot_legacy.py - Phenny scripts ported from old cibot scripts in hubot
"""
# https://github.com/corbisimages/hubot-scripts/blob/master/src/scripts/corbis-event-log.coffee
# https://github.com/quadmiasmo/hubot/blob/master/src/scripts/corbis-event-log.coffee


def view_events(phenny, input):
    url = 'http://dl00testapi01:4242/EventLog/V1/'
    phenny.say("Just get BryanS to do it.")

view_events.rule = r'(corbis )?error(?: me| show)? "?([0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12})"?(?: (?:in|for|from|use) (dev|sqa|stg|prod|[a-z]+)\b)?( archives)?'
view_events.thread = True
view_events.priority = 'high'
