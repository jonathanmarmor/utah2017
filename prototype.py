#!/usr/bin/env python

from collections import OrderedDict


class Meter(object):



class Part(object):
    def __init__(self, instrument_name):
        self.instrument_name = instrument_name
        self.string = '{:<16}'.format(self.instrument_name)
        self.beats = []

    def make_string(self):
        header = self.instrument_name + ':'
        s = '{:<16}'.format(header)
        for b in self.beats:
            if b:
                s += '-'
            else:
                s += ' '
        return s

    def draw(self):
        s = self.make_string()
        print s


class Score(object):
    def __init__(self):
        self.score_order = (
            'violin',
            'flute',
            'oboe',
            'clarinet',
            'alto_saxophone',
            'trumpet',
            'bass',
            'percussion'
        )

        self.score = OrderedDict()
        for inst in self.score_order:
            self.score[inst] = []

    def draw(self):
        for inst, part in self.score.iteritems():




class Prototype(object):
    def __init__(self):
        self.headers =
