import os

from chord_progressions.chord import Chord
from chord_progressions.io.audio import (
    mk_freq_buffer,
    combine_buffers,
    save_audio_buffer,
)
from chord_progressions.pitch import (
    A4,
    MIDI_NOTES,
    get_freq_from_note,
    get_n_overtones_harmonic,
)

AUDIO_DIR = "audio"
TWELVE_TET_DIR = outpath = os.path.join(AUDIO_DIR, "12tet")
JUST_DIR = outpath = os.path.join(AUDIO_DIR, "just")

# See https://en.wikipedia.org/wiki/Pythagorean_tuning
JUST_INTERVAL_RATIOS = {
    "unison": 1,
    "minor second": 256 / 243,
    "major second": 9 / 8,
    "minor third": 32 / 27,
    "major third": 81 / 64,
    "perfect fourth": 4 / 3,
    "diminished fifth": 1024 / 729,
    "augmented fourth": 729 / 512,
    "perfect fifth": 3 / 2,
    "minor sixth": 128 / 81,
    "major sixth": 27 / 16,
    "minor seventh": 16 / 9,
    "major seventh": 243 / 128,
}


def get_pythagorean_frequencies(base_frequency):
    """Create a dict of 13 frequencies using Pythagorean tuning from a given base frequency"""
    return {
        interval: base_frequency * ratio
        for interval, ratio in JUST_INTERVAL_RATIOS.items()
    }


def write_chord_audio_from_freqs(fundamentals, n_overtones, outpath):
    """Synthesize a chord and write a 1-second audio file"""
    freq_buffers = [mk_freq_buffer(f, 1, n_overtones) for f in fundamentals]

    audio = combine_buffers(freq_buffers)

    save_audio_buffer(audio, outpath)
    print(f"Audio saved to {outpath}")


if __name__ == "__main__":
    n_overtones = 10

    # Chords to generate
    chords = [["A4"], ["C#5"], ["E5"], ["A4", "C#5", "E5"]]

    # Synthesize audio of the chords in A440 12-TET
    for note_list in chords:
        chord = Chord(note_list)
        filename = f"{'-'.join(note_list)}_{n_overtones}.wav"
        outpath = os.path.join(TWELVE_TET_DIR, filename)
        chord.to_audio(outpath, n_overtones=n_overtones)

    # Using A4 as the base note corresponds to a midi range of A4 to G#5
    pythagorean_freqs_a4 = get_pythagorean_frequencies(A4)

    # Re-create chord list using just intonation frequencies instead of note names
    just_cs5 = pythagorean_freqs_a4["major third"]
    just_e5 = pythagorean_freqs_a4["perfect fifth"]
    chords_just_freqs = [
        [A4],
        [just_cs5],
        [just_e5],
        [A4, just_cs5, just_e5],
    ]

    # Synthesize audio of the chords in just intonations
    for freq_list in chords_just_freqs:
        filename = f"{'-'.join([str(f) for f in freq_list])}_{n_overtones}.wav"
        just_outpath = os.path.join(JUST_DIR, filename)
        write_chord_audio_from_freqs(freq_list, n_overtones, just_outpath)

    # Create tables of notes with their first N overtones
    note_names = MIDI_NOTES[MIDI_NOTES.index("A4") : MIDI_NOTES.index("G#5")]

    print("12-TONE EQUAL TEMPERAMENT\n")
    for note in note_names:
        f = get_freq_from_note(note)
        freqs = get_n_overtones_harmonic(f, n_overtones)
        print(note, "\t", "\t".join([str(round(i, 2)) for i in freqs]))

    # Just intonation using pythagorean tuning
    print("\n\nJUST INTONATION (PYTHAGOREAN TUNING)\n")
    for interval, f in pythagorean_freqs_a4.items():
        freqs = get_n_overtones_harmonic(f, n_overtones)
        print(interval, "\t", "\t".join([str(round(i, 2)) for i in freqs]))
