#!/usr/bin/env python

import math

from notation_tools import Notation
from instrument_data import instrument_data
import utils


def range16ths(start, end, step=.25):
    return [n / 4.0 for n in xrange(int(start * 4), int(end * 4), int(step * 4))]


def meter_position(tick):
    position_within_beat, beat = math.modf(tick)
    beat = int(beat)
    beat_within_bar = beat % 4
    bar_number = beat // 4
    return bar_number, beat_within_bar, position_within_beat


def beats_to_seconds(beats, bpm=60):
    return beats / (bpm / 60.0)


def pitches_to_pitchclasses(pitches):
    pitchclasses = [p % 12 for p in pitches]
    pitchclasses = list(set(pitchclasses))
    pitchclasses.sort()
    pitchclasses = tuple(pitchclasses)
    return pitchclasses


def get_inversions(pitchclasses):
    inversions = []
    for p1 in pitchclasses:
        inversion = [(p2 - p1) % 12 for p2 in pitchclasses]
        inversion.sort()
        inversions.append(tuple(inversion))
    return inversions


def make_allowed_harmonies():
    allowed_harmonies_1st_inversions = [
        # Just a quick draft
        (0, ),
        # (0, 2),
        # (0, 3),
        (0, 4),
        (0, 5),
        (0, 4, 7),
        (0, 3, 7),
        (0, 5, 7),
        (0, 3, 5),
        (0, 2, 5),
        # (0, 3, 6),
        # (0, 4, 8),
        (0, 2, 4),
        # (0, 2, 6),
        (0, 4, 7, 11),
        (0, 4, 7, 10),
        (0, 3, 7, 10),
        (0, 5, 7, 10),
        (0, 2, 5, 7),
        (0, 2, 4, 7),
        (0, 2, 3, 7),
        (0, 3, 5, 7),
        # (0, 3, 6, 9),
        # (0, 2, 4, 8),
        (0, 2, 4, 7, 11),
        (0, 2, 4, 7, 10),
        (0, 2, 3, 7, 10),
        (0, 2, 4, 6, 8, 10),
        (0, 2, 4, 5, 7, 11),
        (0, 2, 4, 5, 7, 10),
        (0, 2, 3, 5, 7, 10),
    ]
    allowed_harmonies = []
    for harmony in allowed_harmonies_1st_inversions:
        for root in range(12):
            transposed_harmony = tuple([(p + root) % 12 for p in harmony])
            allowed_harmonies.append(transposed_harmony)

    # for harmony in allowed_harmonies_1st_inversions:
    #     inversions = get_inversions(harmony)
    #     allowed_harmonies.extend(inversions)
    return allowed_harmonies


allowed_harmonies = make_allowed_harmonies()


def is_harmony_allowed(pitches):
    return tuple(pitches_to_pitchclasses(pitches)) in allowed_harmonies


class Tick(object):
    def __init__(self, tick):
        self.tick = tick
        self.bar_number, self.beat_within_bar, self.position_within_beat = meter_position(tick)


class Note(object):
    def __init__(self, pitch=None, duration=0.0):
        self.pitch = pitch
        self.duration = duration

    def __repr__(self):
        return '<Note - pitch: {} duration: {}>'.format(self.pitch, self.duration)


class Instrument(list):
    def __init__(self, inst_name):
        self.name = inst_name
        self.abbreviation = instrument_data[self.name]['abbreviation']
        self.range = instrument_data[self.name]['range']
        self._make_registers()

    def __repr__(self):
        return '<full_movie.Instrument: {}>'.format(self.name)

    def _make_registers(self, n_chunks=7):
        self.lowest_note = self.range[0]
        self.highest_note = self.range[-1]

        separators = []
        for i in range(int(n_chunks) + 1):
            separator = i * (len(self.range) / float(n_chunks))
            separators.append(separator)

        registers = []
        for a, b in utils.pairwise(separators):
            chunk = [p for i, p in enumerate(self.range) if a <= i < b]
            registers.append(chunk)

        self.middle_register = registers[3]  # assuming 7 divisions
        self.highest_register = registers[-1]
        self.lowest_register = registers[0]
        self.safe_register = utils.flatten(registers[1:-1])
        self.very_safe_register = utils.flatten(registers[2:-2])

    def duration(self):
        return sum([note.duration for note in self])

    def get_tick(self):
        return Tick(self.duration())

    def add_note(self, pitch=None, duration=0.0):
        self.append(Note(pitch=pitch, duration=duration))

    def get_at_tick(self, tick):
        duration = 0
        for note in self:
            if duration <= tick < duration + note.duration:
                return note
            duration += note.duration


class Music(object):
    def __init__(self, title='Full Movie', starting_tempo_bpm=160):
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
        self.title = title
        self.composer = 'Jonathan Marmor'
        self.time_signature = None
        self.starting_tempo_bpm = starting_tempo_bpm
        self.starting_tempo_quarter_duration = 1.0

        self._setup_parts()


    def _setup_parts(self):
        # Instantiate instruments/parts and make them accessible via Music
        self.instruments = []
        self.grid = {}
        for inst_name in self.instrument_names:
            instrument = Instrument(inst_name)
            setattr(self, instrument.name, instrument)
            setattr(self, instrument.abbreviation, instrument)
            self.instruments.append(instrument)
            self.grid[inst_name] = instrument

    def duration(self):
        return max(instrument.duration() for instrument in self.instruments)

    def get_at_tick(self, tick):
        result = {}
        for instrument in self.instruments:
            result[instrument.name] = instrument.get_at_tick(tick)
        return result

    def notate(self):
        self.notation = Notation(
            instrument_names=self.instrument_names,
            title=self.title,
            composer=self.composer,
            time_signature=self.time_signature,
            starting_tempo_bpm=self.starting_tempo_bpm,
            starting_tempo_quarter_duration=self.starting_tempo_quarter_duration
        )

        for instrument in self.instruments:
            notation_instrument = self.notation.instruments_by_name[instrument.name]
            for note in instrument:
                notation_instrument.add_note(note.pitch, note.duration)

        self.notation.show()
