#!/usr/bin/env python

import random

from notation_tools import make_music21_score, make_music21_note, show


score = make_music21_score(
    time_signature=None,
    starting_tempo_bpm=60,
    starting_tempo_quarter_duration=1.0,
    instrument_names=(
        'violin',
        'flute',
        'oboe',
        'clarinet',
        'alto_saxophone',
        'trumpet',
        'bass',
        'percussion'
    )
)

violin, flute, oboe, clarinet, alto_saxophone, trumpet, bass, percussion = score.parts
instruments = [violin, flute, oboe, clarinet, alto_saxophone, trumpet, bass, percussion]

violin.range = range(55, 96)
flute.range = range(60, 97)
oboe.range = range(59, 87)
clarinet.range = range(50, 90)
alto_saxophone.range = range(49, 81)
trumpet.range = range(52, 83)
bass.range = range(28, 61)


### Make Music


class Part(object):
    def __init__(self, cycle, start, duration, pitch='None Yet'):
        self.cycle = cycle
        self.start = start
        self.duration = duration

        self.playing = [position % cycle.duration for position in range(start, start + duration)]
        self.rests = [position % cycle.duration for position in range(start + duration, start + cycle.duration)]

        self.by_index = []
        self.binary = []
        self.drawing = ''
        for i in range(cycle.duration):
            if i in self.playing:
                self.by_index.append(pitch)
                self.binary.append(1)
                self.drawing += '-'
            else:
                self.by_index.append('rest')
                self.binary.append(0)
                self.drawing += ' '


class Cycle(object):
    def __init__(self, duration=16):
        self.duration = duration
        self.parts = []
        self.by_index = []
        for _ in range(duration):
            self.by_index.append([])

    def add_part(self, start, duration, pitch='None Yet'):
        if duration > self.duration:
            raise Exception('Part duration is longer than cycle duration')

        part = Part(self, start, duration, pitch=pitch)
        self.parts.append(part)
        self.by_index.append(part.by_index)

    def draw(self):
        for part in self.parts:
            print part.drawing


from random import randint


cycle = Cycle(16)

for _ in range(randint(2, 8)):
    cycle.add_note(randint(0, 15), randint(2, 15), pitch=randint(0, 11))

cycle.draw()

for _ in range(4):
    for i, part in enumerate(cycle.notes):
        instrument = instruments[i]
        for pitch in part.by_index:
            note = make_music21_note(pitch, .25)
            instrument.append(note)










# scale = [0, 2, 4, 7, 9]

# def add_note(instrument, pitch_options, duration_options):
#     duration = random.choice([0.5, 1.0, 1.5, 2.0])
#     pitch = None
#     if random.random() < .8:
#         pitch_options = [p for p in pitch_options if p % 12 in scale]
#         if instrument.notesAndRests and instrument.notesAndRests[-1].isNote:
#             previous_pitch = instrument[-1].ps
#             pitch_options = [p for p in pitch_options if abs(previous_pitch - p) < 5]
#         pitch = random.choice(pitch_options)
#     note = make_music21_note(pitch, duration)
#     instrument.append(note)


# for _ in range(40):
#     duration_options = [0.5, 1.0, 1.0, 1.0, 1.5, 1.5, 2.0, 2.5]
#     for i in instruments[:-1]:
#         add_note(i, i.range, duration_options)

show(score)
