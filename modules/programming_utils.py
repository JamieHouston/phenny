#!/usr/bin/env python
# """
# hubot_legacy.py - Phenny scripts ported from old cibot scripts in hubot
# """


# def parse_regex(phenny, input):
#     try:
#         target = input.group(1)
#         if target:
#             phenny.say("http://wiki.corbis.com/index.php?title={0}".format(target))
#         else:
#             phenny.say("fail")
#     except IndexError:
#         phenny.say("missing a month or something important like that")
# parse_regex.rule = r'(?i)(?:analytics|google analytics|GA analytics|GA-reports) (January|February|March|April|May|June|July|August|September|October|November|December)'
# parse_regex.priority = 'low'
