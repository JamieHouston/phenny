#!/usr/bin/env python
"""
markov.py - Markov List
Attempts to put together a list of what people say and say it back in the correct syntax
"""

import os
import pickle
import random
import re
#import pdb


class Markov(object):
    """
    Hacking on a markov chain bot - based on:
    http://code.activestate.com/recipes/194364-the-markov-chain-algorithm/
    http://github.com/ericflo/yourmomdotcom
    """
    messages_to_generate = 5
    chattiness = .01
    max_words = 15
    chain_length = 2
    stop_word = '\n'
    filename = 'markov.db'
    last = None

    def __init__(self):
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            fh = open(self.filename, 'rb')
            self.word_table = pickle.loads(fh.read())
            fh.close()
        else:
            self.word_table = {}

    def _save_data(self):
        #pdb.set_trace()
        fh = open(self.filename, 'w')
        fh.write(pickle.dumps(self.word_table))
        fh.close()

    def split_message(self, message):
        words = message.split()
        if len(words) > self.chain_length:
            words.extend([self.stop_word] * self.chain_length)
            for i in range(len(words) - self.chain_length):
                yield (words[i:i + self.chain_length + 1])

    def generate_message(self, person, size=15, seed_key=None):
        person_words = len(self.word_table.get(person, {}))
        if person_words < size:
            return

        if not seed_key:
            seed_key = random.choice(self.word_table[person].keys())

        message = []
        for i in xrange(self.messages_to_generate):
            words = seed_key
            gen_words = []
            for i in xrange(size):
                if words[0] == self.stop_word:
                    break

                gen_words.append(words[0])
                try:
                    words = words[1:] + (random.choice(self.word_table[person][words]),)
                except KeyError:
                    break

            if len(gen_words) > len(message):
                message = list(gen_words)

        return ' '.join(message)

    def imitate(self, phenny, input):
        person = input.group(1).strip()[:10]
        if person != phenny.nick:
            return self.generate_message(person)

    def cite(self, phenny, input):
        if self.last:
            return self.last

    def sanitize_message(self, message):
        """Convert to lower-case and strip out all quotation marks"""
        return re.sub('[\"\']', '', message.lower())

    def is_ping(self, message, phenny):
        return re.match('^%s[:,\s]' % phenny.nick, message) is not None

    def fix_ping(self, message, phenny):
        return re.sub('^%s[:,\s]\s*' % phenny.nick, '', message)

    def log(self, phenny, input):
        #pdb.set_trace()
        sender = input.nick[:10]
        message = input.group(0)
        self.word_table.setdefault(sender, {})

        if message.startswith('/'):
            return

        try:
            say_something = self.is_ping(message, phenny) or sender != phenny.nick and random.random() < self.chattiness
        except AttributeError:
            say_something = False
        messages = []
        seed_key = None

        if self.is_ping(message, phenny):
            message = self.fix_ping(message, phenny)

        for words in self.split_message(self.sanitize_message(message)):
            key = tuple(words[:-1])
            if key in self.word_table:
                self.word_table[sender][key].append(words[-1])
            else:
                self.word_table[sender][key] = [words[-1]]

            if self.stop_word not in key and say_something:
                for person in self.word_table:
                    if person == sender:
                        continue
                    if key in self.word_table[person]:
                        generated = self.generate_message(person, seed_key=key)
                        if generated:
                            messages.append((person, generated))

        if len(messages):
            self.last, message = random.choice(messages)
            return message

    def load_log_file(self, filename):
        fh = open(filename, 'r')
        logline_re = re.compile('<\s*(\w+)>[^\]]+\]\s([^\r\n]+)[\r\n]')
        for line in fh.readlines():
            match = logline_re.search(line)
            if match:
                sender, message = match.groups()
                self.log(sender, message, '', False, None)

    def load_text_file(self, filename, sender):
        fh = open(filename, 'r')
        for line in fh.readlines():
            self.log(sender, line, '', False, None)

#    def __del__(self):
#        self._save_data()


# markov_bot = None

# def get_markov():
#     # if markov_bot is None:
#     #     markov_bot = Markov()
#     # return markov_bot
#     return Markov()

# def markov_imitate(phenny, input):
#     get_markov().imitate(phenny, input)
# markov_imitate.commands = ['imitate']

# def markov_cite(phenny, input):
#     get_markov().cite(phenny, input)
# markov_cite.commands = ['city']

# def markov_master(phenny, input):
#     marvin_kov = get_markov()
#     marvin_kov.log(phenny, input)
#     marvin_kov._save_data()
# markov_master.rule = r'(.*)'


if __name__ == '__main__':
    print __doc__.strip()
