#!/usr/bin/env python

import random

from notation_tools import Notation
from instrument_ranges import instrument_ranges


notes = [
    (None, 3),
    (64, .5),
    (60, .5),
    (69, 1.0 / 3),
    (72, 1.0 / 3),
    (69, 1.0 / 3),
    (67, .5),
    (72, 1),
    (72, .5),
    (67, 1.0 / 3),
    (72, 1.0 / 3),
    (67, 1.0 / 3),
    (66, .5),
    (None, .5),
    (69, .5),
    (67, .5),
    (None, .5),
    (64, .5),
    (60, .5),
    (None, .5),
    (65, .5),
    (67, .5),
    (63, .5),
    (64, .5),
    (60, .5),
    (57, .5),
    (None, 1)
]


class Instrument(list):
    def __init__(self, inst_name):
        self.name = inst_name
        self.range = instrument_ranges[self.name]

    def duration(self):
        return sum([note[-1] for note in self])


class Music(dict):
    def __init__(self):
        self.instrument_names = (
            'violin',
            'flute',
            'oboe',
            'clarinet',
            'alto_saxophone',
            'trumpet',
            'bass',
            # 'percussion'
        )
        self.title = 'Full Movie'
        self.composer = 'Jonathan Marmor'
        self.time_signature = None
        self.starting_tempo_bpm = 160
        self.starting_tempo_quarter_duration = 1.0

        self._setup_parts()


    def _setup_parts(self):
        # Instantiate parts and instruments and make them accessible via Piece
        self.instruments = []
        self.grid = {}
        for inst_name in self.instrument_names:
            instrument = Instrument(inst_name)
            setattr(self, inst_name, instrument)
            self.instruments.append(instrument)
            self.grid[inst_name] = instrument

    def duration(self):
        return max(instrument.duration() for instrument in self.instruments)

    def make_test_data(self):
        for i in self.instrument_names:
            self.grid[i] = ['{}{}'.format(i[0], str(x)) for x in range(5)]

    def get(self, instruments, start=0, end=None):
        """
            m = Music()

            # == Instrument selection ==

            # No args gets all instruments
            >>> m.get()
            {'alto_saxophone': [],
             'bass': [],
             'clarinet': [],
             'flute': [],
             'oboe': [],
             'trumpet': [],
             'violin': []}

            # One instrument name string gets that part, not wrapped in a dict
            >>> m.get('oboe')
            []

            # Two or more instrument name strings gets those parts, wrapped in a dict
            >>> m.get('oboe', 'bass')
            {'bass': [],
             'oboe': []}

            # Two or more instrument name strings in a list or tuple gets those  parts, wrapped in a dict
            >>> m.get(['oboe', 'bass'])
            {'bass': [],
             'oboe': []}

            # == time slices ==

            >>> m = Music()
            >>> for i in m.instrument_names:
                m.grid[i] = ['{}{}'.format(i[0], str(x)) for x in range(5)]

            # No args get all instruments' complete parts
            >>> m.get()
            {'alto_saxophone': ['a0', 'a1', 'a2', 'a3', 'a4'],
             'bass': ['b0', 'b1', 'b2', 'b3', 'b4'],
             'clarinet': ['c0', 'c1', 'c2', 'c3', 'c4'],
             'flute': ['f0', 'f1', 'f2', 'f3', 'f4'],
             'oboe': ['o0', 'o1', 'o2', 'o3', 'o4'],
             'trumpet': ['t0', 't1', 't2', 't3', 't4'],
             'violin': ['v0', 'v1', 'v2', 'v3', 'v4']}

            # No instrument args, and one
            >>> m.get(1)


        """

        if instruments is 'all':
            instruments = self.instrument_names
        if end is None:
            end = self.get_current_duration()

        result = {}
        for i in instruments:
            result[i] = self.grid[i][start:end]

        return result
        # return {i:self.grid[i][start:end] for i in instruments}

    def get_current_duration(self):
        return len(self.grid[self.instrument_names[0]])

    def notate(self):
        self.notation = Notation(
            instrument_names=self.instrument_names,
            title=self.title,
            composer=self.composer,
            time_signature=self.time_signature,
            starting_tempo_bpm=self.starting_tempo_bpm,
            starting_tempo_quarter_duration=self.starting_tempo_quarter_duration
        )

        for instrument_name in self.grid:
            part = self.grid[instrument_name]
            notation_instrument = self.notation.instruments_by_name[instrument_name]
            for pitch, duration in part:
                notation_instrument.add_note(pitch, duration)

        self.notation.show()

    def make_random_notes(self):
        mode = [0, 2, 4, 5, 7, 9, 11]
        root = random.choice(range(12))

        scales = []
        for _ in range(8):
            root_change = random.choice([-1, 1, 6])
            root = (root + root_change) % 12
            scale = [(root + p) % 12 for p in mode]
            scales.append(scale)

        for instrument in self.instruments:
            previous_pitch = instrument.range[len(instrument.range) / 2]
            while instrument.duration() <= 64:

                if instrument.duration() < 16:
                    scale = scales[0]
                elif instrument.duration() < 32:
                    scale = scales[1]
                elif instrument.duration() < 48:
                    scale = scales[2]
                elif instrument.duration() < 64:
                    scale = scales[3]

                if random.random() > .5:
                    pitch = None
                    duration = random.randint(1, 16) / 4.0
                else:
                    pitch_options = range(previous_pitch - 3, previous_pitch + 4)
                    pitch_options.remove(previous_pitch)
                    pitch_options = [p for p in instrument.range if p in pitch_options and p % 12 in scale]
                    pitch = random.choice(pitch_options)
                    duration = random.randint(1, 8) / 4.0

                instrument.append((pitch, duration))


def main():
    music = Music()

    music.make_random_notes()

    # music.grid['alto_saxophone'] = notes
    music.notate()


if __name__ == '__main__':
    main()
