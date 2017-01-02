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
oboe.range = range(59, 92)
clarinet.range = range(50, 90)
alto_saxophone.range = range(49, 81)
trumpet.range = range(52, 83)
bass.range = range(28, 61)

### Make Music

scale = [0, 2, 4, 7, 9]

def add_note(instrument, pitch_options, duration_options):
    duration = random.choice([0.5, 1.0, 1.5, 2.0])
    pitch = None
    if random.random() < .8:
        pitch_options = [p for p in pitch_options if p % 12 in scale]
        if instrument.notesAndRests and instrument.notesAndRests[-1].isNote:
            previous_pitch = instrument[-1].ps
            pitch_options = [p for p in pitch_options if abs(previous_pitch - p) < 5]
        pitch = random.choice(pitch_options)
    note = make_music21_note(pitch, duration)
    instrument.append(note)


for _ in range(40):
    duration_options = [0.5, 1.0, 1.0, 1.0, 1.5, 1.5, 2.0, 2.5]
    for i in instruments[:-1]:
        add_note(i, i.range, duration_options)

show(score)
