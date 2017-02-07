import datetime

import music21


def show(stream):
    notation_gui_app = '/Applications/MuseScore 2.app'
    # notation_gui_app = '/Applications/Sibelius 7.5.app'
    stream.show('musicxml', notation_gui_app)


instrument_directory = {
    'violin': {'class': music21.instrument.Violin, 'name': 'Violin', 'abbreviation': 'vln'},
    'flute': {'class': music21.instrument.Flute, 'name': 'Flute', 'abbreviation': 'f'},
    'oboe': {'class': music21.instrument.Oboe, 'name': 'Oboe', 'abbreviation': 'ob'},
    'clarinet': {'class': music21.instrument.Clarinet, 'name': 'Clarinet', 'abbreviation': 'cl'},
    'alto_saxophone': {'class': music21.instrument.Saxophone, 'name': 'Alto Saxophone', 'abbreviation': 'sx'},
    'trumpet': {'class': music21.instrument.Trumpet, 'name': 'Trumpet', 'abbreviation': 'tpt'},
    'bass': {'class': music21.instrument.Bass, 'name': 'Fretless Bass', 'abbreviation': 'b', 'clef': music21.clef.BassClef},
    'percussion': {'class': music21.instrument.Percussion, 'name': 'Percussion', 'abbreviation': 'perc'}
}

instrument_ranges = {
    'violin': range(55, 96),
    'flute': range(60, 97),
    'oboe': range(59, 87),
    'clarinet': range(50, 90),
    'alto_saxophone': range(49, 81),
    'trumpet': range(52, 83),
    'bass': range(28, 61),
    'percussion': None
}


def make_music21_score(time_signature=None, starting_tempo_bpm=60,
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
        )):
    timestamp = datetime.datetime.utcnow()
    metadata = music21.metadata.Metadata()
    metadata.title = 'Utah 2017'
    metadata.composer = 'Jonathan Marmor'
    metadata.date = timestamp.strftime('%Y/%m/%d')

    score = music21.stream.Score()
    score.insert(0, metadata)

    parts = []  # Unnecessary?
    for name in instrument_names:
        instrument = instrument_directory[name]

        part = music21.stream.Part()

        metronome_mark = music21.tempo.MetronomeMark(
            number=starting_tempo_bpm,
            referent=music21.duration.Duration(starting_tempo_quarter_duration)
        )
        part.append(metronome_mark)

        if time_signature:
            # Should be a string like '12/8'
            music21_time_signature = music21.meter.TimeSignature(time_signature)
            part.append(music21_time_signature)

        m21_instrument = instrument['class']()
        m21_instrument.partName = instrument['name']
        m21_instrument.partAbbreviation = instrument['abbreviation']

        part.insert(0, m21_instrument)

        clef = instrument.get('clef')
        if clef:
            part.append(clef())

        parts.append(part)  # Unnecessary?
        score.insert(0, part)

    return score


def make_music21_note(pitch_number=None, duration=1.0):
    if pitch_number == None or pitch_number == 'rest':
        n = music21.note.Rest()
    elif isinstance(pitch_number, list):
        pitches = [music21.pitch.Pitch(p) for p in pitch_number]
        for p in pitches:
            if p.accidental.name is 'natural':
                p.accidental = None
        n = music21.chord.Chord(pitches)
    else:
        p = music21.pitch.Pitch(pitch_number)
        if p.accidental.name is 'natural':
            p.accidental = None
        n = music21.note.Note(p)

    d = music21.duration.Duration()
    d.quarterLength = duration
    n.duration = d

    return n


class Piece(object):
    def __init__(
        self,
        instrument_names,
        time_signature=None,
        starting_tempo_bpm=60,
        starting_tempo_quarter_duration=1.0
        ):

        self.instrument_names = instrument_names

        self.score = make_music21_score(
            time_signature=time_signature,
            starting_tempo_bpm=starting_tempo_bpm,
            starting_tempo_quarter_duration=starting_tempo_quarter_duration,
            instrument_names=instrument_names
        )

        self.instruments = []
        for inst_name, part in zip(self.instrument_names, self.score.parts):
            setattr(self, inst_name, part)
            self.instruments.append(part)

            getattr(self, inst_name).range = instrument_ranges[inst_name]

    def show(self):
        show(self.score)
