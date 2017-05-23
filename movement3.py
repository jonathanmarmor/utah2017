#!/usr/bin/env python

import random

from music_tools import Music
from utils import pairwise


def get_intervals(pitches):
    ps = list(set(pitches))
    ps.sort()
    return [b - a for a, b in pairwise(ps)]



class Movement3(object):
    def __init__(self):
        self.music = m = Music()

        self.winds = [m.f, m.ob, m.cl]

        self.register = range(66, 87)

        self.first()

        self.go(150)

        self.music.notate()


    def first(self):
        self.music.ob.add_note(pitch=72, duration=1.0)
        self.music.cl.add_note(pitch=73, duration=1.0)
        self.music.f.add_note(pitch=74, duration=1.0)


    def go(self, ticks=50):
        for tick in range(ticks):
            self.next()

    def next(self):

        last_chord = [w[-1].pitch for w in self.winds]
        print last_chord, get_intervals(last_chord)

        changing = random.choice(self.winds)
        not_changing = [w for w in self.winds if w is not changing]

        move = move = random.choice([1, -1])
        if random.random() < .1:
            move = random.choice([2, -2])

        new_pitch = changing[-1].pitch + move
        if new_pitch not in changing.range:
            move = -move
            new_pitch = changing[-1].pitch + move

        changing.add_note(pitch=new_pitch, duration=1.0)

        for i in not_changing:
            i[-1].duration += 1.0

        # for w in winds:
        #     print w[-1].pitch, w[-1].pitch in w.range


if __name__ == '__main__':
    m3 = Movement3()
