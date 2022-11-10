# MPC Brightness

## Usage

Install [Essentia](https://essentia.upf.edu/installing.html).

Run `analyze.py` to compute spectral centroid and inharmonicity for the survey audio.

Run `synthesize.py` to create (experimental) audio files for the survey. Note that this script depends on
the [chord-progressions](https://github.com/p3zo/chord-progressions) library which
is not yet published to PyPI. You must that clone that repo and pip install it locally.
