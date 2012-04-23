# #!/usr/bin/env python
# """
# achievement.py - Unlock achievements
# Bonuses for employees that do stuff
# """


# class Achievement(object):
#     template = """
#   /.–==*==–.\\
#  ( |      #| ) %(announcement)s
#   ):      ':(
#     `·…_…·´    %(title)s
#       `H´      %(subtitle)s
#      _.U._     %(message)s
#     [_____]"""
#     title = None
#     subtitle = None
#     message = None

#     def configure(self, options, conf):
#         pass

#     def finalize(self, data, result):
#         pass

#     def announcement(self, info=None):
#         template = self.template
#         try:
#             template = template.decode('utf-8')
#         except AttributeError:
#             pass
#         return template % {'announcement': "Achievement unlocked!",
#                            'title': self.title or "",
#                            'subtitle': self.subtitle or "",
#                            'message': self.message or ""}

# class NightShift(Achievement):
#     key = 'builtin:night-shift'
#     title = "Night Shift"
#     message = "You're on pretty late..."
#     template = """
#      .·:´   |   *
#  * ·::·   – ¤ –      %(announcement)s
#   :::::     |
#   :::::.        .:   %(title)s
#    :::::`:·..·:´:'   %(subtitle)s
#     `·::::::::·´  *  %(message)s
#         ˘˘˘˘"""

#     shift_start = time(0, 0)
#     shift_end = time(5, 0)

#     def finalize(self, data, result):
#         if (data['result.tests'] and data['result.success'] and
#             data['history'] and
#             not data['history'][-1].get('result.success', True) and
#             self.shift_start <= data['time.start'].time() < self.shift_end and
#             self.shift_start <= data['time.finish'].time() < self.shift_end):
#             data.unlock(self)