#!/usr/bin/env python
"""
tools.py - Phenny Tools
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""


# Dynamic class
# Instantiate with bla=Dyamic(x=1, y=2)
# then just set of call like bla.foo = True
class Dynamo:
    __init__ = lambda self, **kw: setattr(self, '__dict__', kw)


def deprecated(old):
    def new(phenny, input, old=old):
        self = phenny
        origin = type('Origin', (object,), {
            'sender': input.sender,
            'nick': input.nick
        })()
        match = input.match
        args = [input.bytes, input.sender, '@@']

        old(self, origin, match, args)
    new.__module__ = old.__module__
    new.__name__ = old.__name__
    return new

if __name__ == '__main__':
    print __doc__.strip()
