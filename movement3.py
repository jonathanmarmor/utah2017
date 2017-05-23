#!/usr/bin/env python

import random

from music_tools import Music
from utils import pairwise, weighted_choice


ALLOWED_HARMONIES = {
    (0, 1, 2): 1.0,

    (0, 1, 3): 1.0,
    (0, 2, 3): 1.0,

    (0, 1, 4): .2,
    (0, 3, 4): .2,

    (0, 1, 5): .1,
    (0, 4, 5): .1,

    (0, 1, 6): .1,
    (0, 5, 6): .1,

    (0, 1, 7): .1,
    (0, 6, 7): .1,

    (0, 1, 8): .1,
    (0, 7, 8): .1,

    (0, 1, 9): .001,
    (0, 8, 9): .001,

    (0, 1, 10): .001,
    (0, 9, 10): .001,

    (0, 1, 11): .1,
    (0, 10, 11): .1,

    (0, 1, 12): .2,
    (0, 11, 12): .2,

    (0, 1, 13): .2,
    (0, 12, 13): .2,

    (0, 1, 14): .1,
    (0, 13, 14): .1,
}


DISTANCE_WEIGHTS = [.25, 1.0, .8, ] + [1.0 / (2.0 ** x) for x in range(3, 30)]


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
        self.music.ob.add_note(pitch=72, duration=random.choice([2, 3, 4]))
        self.music.cl.add_note(pitch=73, duration=random.choice([2, 3, 4]))
        self.music.f.add_note(pitch=74, duration=random.choice([2, 3, 4]))

    def go(self, ticks=50):
        for tick in range(ticks):
            self.next()

    def next(self):
        changing, not_changing = self.pick_changing_instrument()

        new_pitch = self.pick_new_pitch(changing, not_changing)

        total_event_duration = 0.0
        if random.random() < .5:
            # Add a rest before the next note
            rest_duration = random.choice([1, 1, 1, 2, 2, 3])
            total_event_duration += rest_duration
            changing.add_note(pitch='rest', duration=rest_duration)

        note_duration = random.choice([1, 1, 2])
        total_event_duration += note_duration
        changing.add_note(pitch=new_pitch, duration=note_duration)

        for i in not_changing:
            i[-1].duration += total_event_duration


    def pick_changing_instrument(self):

        # TODO: try prefering picking changing instruments when the other two instruments are playing a minor second
        # previous_chord = [i[-1].pitch for i in self.winds]
        # intervals = get_intervals(previous_chord)


        weights = []
        for inst in self.winds:
            sustain_time = inst.beats_since_last_rest() * (60.0 / self.music.starting_tempo_bpm)

            # weight = (inst.beats_since_last_rest() + 1) ** 2.0
            weight = sustain_time ** 2
            weights.append(weight)

        print weights
        changing = weighted_choice(self.winds, weights)

        # changing = random.choice(self.winds)

        not_changing = [w for w in self.winds if w is not changing]
        return changing, not_changing

    def pick_new_pitch(self, changing, not_changing):

        ### Pick only allowed harmonies
        holdovers = [i[-1].pitch for i in not_changing]
        holdovers.sort()

        previous_pitch = changing.get_last_pitched().pitch

        pitch_options = []
        weights = []
        for pitch_option in changing.range:
            harmony = holdovers + [pitch_option]
            harmony.sort()
            harmony = [ps - harmony[0] for ps in harmony]
            harmony = tuple(harmony)
            if harmony in ALLOWED_HARMONIES:
                pitch_options.append(pitch_option)

                # The further away the new pitch from the previous pitch, the lower the weight
                distance = abs(previous_pitch - pitch_option)
                distance_weight = DISTANCE_WEIGHTS[distance]

                # TODO: make and use harmony weights too
                # harmony_weight = 1.0
                harmony_weight = ALLOWED_HARMONIES[harmony]

                # weight the different weights
                weight = (distance_weight * 1.0) + (harmony_weight * .25)

                weights.append(weight)

                # print harmony, weight

        new_pitch = weighted_choice(pitch_options, weights)
        # new_pitch = random.choice(pitch_options)
        # print




        ### Wander by half and whole steps

        # previous_pitch = changing.get_last_pitched().pitch

        # move = random.choice([1, -1])
        # if random.random() < .2:
        #     move = random.choice([2, -2])

        # new_pitch = previous_pitch + move
        # if new_pitch not in changing.range:
        #     move = -move
        #     new_pitch = previous_pitch + move

        return new_pitch


if __name__ == '__main__':
    m3 = Movement3()
