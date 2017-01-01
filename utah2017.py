#!/usr/bin/env python

import random

from notation_tools import make_music21_score, make_music21_note, show


oboe_notes = range(60, 87)
oboe_notes.remove(61)

bass_notes = range(28, 68)

guitar_notes = range(40, 76)


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


def add_note(instrument, pitch_options, duration_options):
    duration = random.choice([0.5, 1.0, 1.5, 2.0])
    pitch = random.choice(oboe_notes)
    note = make_music21_note(pitch, duration)
    instrument.append(note)


for _ in range(20):
    duration_options = [0.5, 1.0, 1.5, 2.0]

    add_note(violin, oboe_notes, duration_options)
    add_note(oboe, oboe_notes, duration_options)
    add_note(flute, oboe_notes, duration_options)
    add_note(clarinet, oboe_notes, duration_options)
    add_note(alto_saxophone, oboe_notes, duration_options)
    add_note(trumpet, oboe_notes, duration_options)
    add_note(bass, bass_notes, duration_options)

show(score)
