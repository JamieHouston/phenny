def message_join(phenny, input):
    phenny.say("welcome, %s!" % input.nick)
message_join.event = 'JOIN'
message_join.rule = r'.*'
