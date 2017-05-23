#!/usr/bin/env python

import random
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

    def september_song(self):
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
        self.sx.extend([Note(*n) for n in notes])

    def make_random_notes(self, n_bars=16):
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

            tick = instrument.get_tick()
            while tick.bar_number <= n_bars:
                scale == scales[tick.bar_number / 4]

                if random.random() > .5:
                    pitch = None
                    duration = random.choice([1, 1.5, 2])
                else:
                    pitch_options = range(previous_pitch - 3, previous_pitch + 4)
                    pitch_options.remove(previous_pitch)
                    pitch_options = [p for p in instrument.range if p in pitch_options and p % 12 in scale]
                    pitch = random.choice(pitch_options)
                    duration = random.randint(1, 8) / 2.0

                instrument.add_note(pitch, duration)

                tick = instrument.get_tick()

    def big_chord(self):
        mode = [0, 2, 4, 5, 7, 9, 11]
        root = random.choice([0, 7, 5, 2, 10])  # easier keys on C instruments
        scale = [(root + p) % 12 for p in mode]


        # Bass
        b = self.bass
        bass_pitch = 48  # random.choice([p for p in b.range[:13] if p % 12 in scale])

        # Thirds (sax, trumpet)
        sx = self.alto_saxophone
        tpt = self.trumpet

        sx_pitch = 64  # random.choice([p for p in sx.range[8:-8] if p % 12 in scale])
        tpt_pitch = 67

        # Cluster (flute, oboe, clarinet)
        fl = self.flute
        ob = self.oboe
        cl = self.clarinet
        cluster_instruments = [fl, ob, cl]

        fl_pitch = 84
        ob_pitch = 83
        cl_pitch = 81

        # Fifths (violin)
        vln = self.violin
        vln_pitch = [62, 69]


        tick = self.duration()
        bar_number, beat_within_bar, position_within_beat = meter_position(tick)

        # while bar_number <= 16:



        for tick in range(16):
            # Bass
            b.add_note(bass_pitch, 4.0)

            # Thirds
            sx.add_note(sx_pitch, 4.0)
            tpt.add_note(tpt_pitch, 4.0)

            # Cluster
            cl.add_note(cl_pitch, 4.0)
            ob.add_note(ob_pitch, 4.0)
            fl.add_note(fl_pitch, 4.0)

            # Fifths
            vln.add_note(vln_pitch, 4.0)

        '''
        harmonic change pace
        breath pace
        '''

    # def wedge(self):
    #     entrance_order = [self.instruments[index] for index in random.shuffle(range(len(self.instruments)))]

    #     solo = entrance_order[0]
    #     accompanists = entrance_order[1:]
    #     bass = self.bass

    #     # solo ascending
    #     # bass descending
    #     # for rest of accompanists, pick ascending or descending randomly
    #     # solo should ascend pretty high in the instrument range
    #     # bass should descend most of the way down
    #     # everyone else should be more reserved
    #     solo.direction = 'ascending'
    #     for instrument in accompanists:
    #         instrument.direction = random.choice(['ascending', 'descending'])
    #     bass.direction = 'descending'


    #     length, remainder = divmod(len(solo.range), 5)

    #     utils.group(len(solo.range), 5)
    #     solo.range
    #     solo.starting_register_center = random.


    #     for instrument in entrance_order:
    #         instrument.pace = random.choice([.5, 1, 1, 2])

    def check_fragment(self, start=0, end=None):
        if end is None:
            end = self.duration()

        allowed = []
        for tick in xrange(int(start * 12), int(end * 12)):
            tick = tick / 12.0
            notes = self.get_at_tick(tick)

            all_pitches = []
            for name in notes:
                pitches = notes[name].pitch
                if pitches is not 'rest' and pitches is not None:
                    if isinstance(pitches, list):
                        all_pitches.extend(pitches)
                    else:
                        all_pitches.append(pitches)

            allowed.append(is_harmony_allowed(all_pitches))
        return all(allowed)

    def make_lick(self, instrument, duration=4.0, scale=[0, 2, 4, 5, 7, 9, 11]):
        if random.random() < .5:
            opening_rest_duration = random.choice(range16ths(.5, duration - 1.5, .5))
            instrument.add_note(None, opening_rest_duration)

        remaining = duration - instrument.duration()

        lick_total_duration_options = range16ths(1.5, remaining + .5, .5)
        lick_total_duration = random.choice(lick_total_duration_options)

        # how many attacks?
        n_attacks = 1
        if random.random() < .3:
            n_attacks = 2

        if random.random() < .2:
            n_attacks_options = range(1, int(lick_total_duration * 2))
            n_attacks_weights = range(1, len(n_attacks_options) + 1)
            n_attacks = utils.weighted_choice(n_attacks_options, n_attacks_weights)


        # if random.random() < .2:
        #     n_attacks = 1
        # else:
        #     n_attacks_options = range(1, int(lick_total_duration * 2))
        #     n_attacks_weights = range(1, len(n_attacks_options) + 1)
        #     n_attacks = utils.weighted_choice(n_attacks_options, n_attacks_weights)



        # The first attack is in the first index
        attack_indexes = [0]
        attack_index_options = range(1, int(lick_total_duration * 2))

        # pick starting point of the rest of the attacks
        for _ in range(n_attacks - 1):
            i = random.choice(attack_index_options)
            attack_indexes.append(i)
            attack_index_options.remove(i)

        attack_indexes.sort()

        # Get durations of each note
        attack_indexes.append(int(lick_total_duration * 2))
        durations = []
        for start, end in utils.n_wise(attack_indexes, 2):
            dur = end - start
            durations.append(dur / 2.0)


        range_in_key = [p for p in instrument.range[7:-8] if p % 12 in scale]

        # set starting pitch anchor
        initial_pitch = random.choice(range_in_key)
        pitch = initial_pitch
        for d in durations:

            i = range_in_key.index(pitch)
            # movement = random.choice([-1, -1, -1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
            movement = random.choice([-1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            try:
                pitch = range_in_key[i + movement]
            except IndexError:
                pitch = initial_pitch

            # # Temporary. Pick a random pitch.
            # pitch = random.choice([p for p in instrument.range[7:-8] if p % 12 in scale])

            instrument.add_note(pitch, d)


        remaining = duration - instrument.duration()
        if remaining:
            instrument.add_note(None, remaining)

        return instrument

    def extend_with_fragment(self, fragment):
        for fragment_instrument in fragment.instruments:
            instrument = self.grid[fragment_instrument.name]
            instrument.extend(fragment_instrument)

    def make_fragment(self, duration=4.0, scale=[0, 2, 4, 5, 7, 9, 11], n_instruments=8):
        fragment = Music()


        # n_instruments = utils.weighted_choice(n_instruments_options, [w ** 3 for w in n_instruments_options])

        instruments = random.sample(fragment.instruments, n_instruments)

        for instrument in instruments:
            self.make_lick(instrument, duration=duration, scale=scale)

        resting_instruments = [i for i in fragment.instruments if i not in instruments]

        # Put rests in instruments that aren't playing
        for resting_instrument in resting_instruments:
            resting_instrument.add_note(None, duration)

        return fragment

    def make_fragments(self):
        scale = [0, 2, 4, 5, 7, 9, 11]

        n_instruments = 1

        for count in range(2500):

            if random.random() < .15:
                # Change keys
                switch = random.random()
                if switch < .6:
                    # Go up a fifth
                    scale = [(p + 7) % 12 for p in scale]
                elif switch < .9:
                    # Go down a fifth
                    scale = [(p - 7) % 12 for p in scale]
                elif switch < .95:
                    # Go up a whole step
                    scale = [(p + 2) % 12 for p in scale]
                else:
                    # Go down a whole step
                    scale = [(p - 2) % 12 for p in scale]


            # scale = [0, 2, 4, 7, 9]
            # scale = range(12)
            # for _ in range(random.randint(0, 5)):
            #     pc = random.choice(scale)
            #     scale.remove(pc)

            duration = random.choice([3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 6, 6, 7, 8, 8, 8])


            n_instruments_candidate = n_instruments

            if random.random() < .3:
                if n_instruments_candidate == 7:
                    n_instruments_candidate = 1
                else:
                    n_instruments_candidate += 1

            fragment = self.make_fragment(duration=duration, scale=scale, n_instruments=n_instruments_candidate)
            print count,

            if fragment.check_fragment():
                print
                print 'Whoa!!!!'
                self.extend_with_fragment(fragment)
                n_instruments = n_instruments_candidate



def main():
    music = Music()

    music.make_fragments()
    # music.big_chord()
    # music.make_random_notes()
    # music.september_song()

    music.notate()


if __name__ == '__main__':
    main()
