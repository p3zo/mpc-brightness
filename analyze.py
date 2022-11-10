import glob
import os

import essentia.standard as es
import pandas as pd
from essentia import Pool

AUDIO_DIR = "audio/Sounds-v0"

SAMPLE_RATE = 44100

if __name__ == "__main__":

    df = pd.DataFrame()

    for fp in glob.glob(os.path.join(AUDIO_DIR, "*/*.wav")):
        sound_id = (
            "-".join(os.path.splitext(fp)[0].split("/")[-2:]).replace(" ", "").lower()
        )
        print(sound_id)

        pitch = int(sound_id.split("hz")[0])

        # Load audio
        x = es.MonoLoader(filename=fp, sampleRate=SAMPLE_RATE)()

        # Create the pool and instantiate the necessary algorithms
        pool = Pool()
        w = es.Windowing()
        spec = es.Spectrum()

        centroid = es.Centroid(range=22050)

        frame_size = 1024
        peaks = es.SpectralPeaks(
            orderBy="frequency", minFrequency=SAMPLE_RATE / frame_size
        )

        harmPeaks = es.HarmonicPeaks()
        inharmonicity = es.Inharmonicity()

        # Compute the features for all frames in our audio and add them to the pool
        for frame in es.FrameGenerator(x, frameSize=frame_size, hopSize=512):
            # Get the spectrum
            s = spec(w(frame))

            # Compute spectral centroid
            c = centroid(s)

            # Compute inharmonicity
            peakFreqs, peakMags = peaks(s)
            harmFreqs, harmPeakMags = harmPeaks(peakFreqs, peakMags, pitch)
            i = inharmonicity(harmFreqs, harmPeakMags)

            pool.add("spectral_centroid", c)
            pool.add("inharmonicity", i)

        # Aggregate the results
        aggPool = es.PoolAggregator(defaultStats=["mean"])(pool)

        fdf = pd.DataFrame(
            [
                [
                    sound_id,
                    aggPool["spectral_centroid.mean"],
                    aggPool["inharmonicity.mean"],
                ]
            ],
            columns=["sound_id", "spectral_centroid", "inharmonicity"],
        )

        df = pd.concat([df, fdf])

    outpath = "analysis.csv"
    df.to_csv(outpath, index=False)
    print(f"Wrote {outpath}")
