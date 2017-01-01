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

violin.range = range(55, 101)
flute.range = range(60, 97)
oboe.range = range(59, 92)
clarinet.range = range(50, 90)
alto_saxophone.range = range(49, 81)
trumpet.range = range(52, 83)
bass.range = range(28, 61)


def add_note(instrument, pitch_options, duration_options):
    duration = random.choice([0.5, 1.0, 1.5, 2.0])
    pitch = random.choice(pitch_options)
    note = make_music21_note(pitch, duration)
    instrument.append(note)


for _ in range(20):
    duration_options = [0.5, 1.0, 1.5, 2.0]

    for i in instruments[:-1]:
        add_note(i, i.range, duration_options)

show(score)
