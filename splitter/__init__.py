import argparse
import os
import pathlib
import sys
import wave

import speech_recognition as sr

parser = argparse.ArgumentParser(
    prog="Audio Splitter",
    description="splits a WAV file into several overlapping segments in WAV format",
)
parser.add_argument("audio_file", type=argparse.FileType("rb"))
parser.add_argument(
    "-d", "--segment-duration", dest="segment_duration", type=float, default=8.0
)
parser.add_argument(
    "-o", "--output-dir", dest="output_dir", default="out", type=pathlib.Path
)
parser.add_argument("-s", "--start", dest="start_seconds", type=float, default=0.0)
parser.add_argument("-e", "--end", dest="end_seconds", type=float, default=float("inf"))


def ms(seconds: int) -> int:
    return seconds * 1000


def main() -> int:
    args = parser.parse_args()

    audio_file = args.audio_file
    segment_duration = args.segment_duration
    output_dir = args.output_dir

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    with sr.AudioFile(audio_file) as source:
        audio_data = sr.Recognizer().record(source)

    start = args.start_seconds
    end = start + segment_duration
    while end <= args.end_seconds:
        segment = audio_data.get_segment(ms(start), ms(end))
        if audio := segment.get_raw_data():
            with wave.open(
                str(output_dir.joinpath(f"clip_{start}s-{end}s.wav")), "wb"
            ) as wavfile:
                wavfile.setparams(
                    # see https://docs.python.org/3/library/wave.html#wave.Wave_write.setparams
                    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
                    # nchannels is 1 because `AudioData` is mono
                    (1, segment.sample_width, segment.sample_rate, 0, "NONE", "NONE")
                )
                wavfile.writeframes(audio)

            start += segment_duration // 2
            end = start + segment_duration
        else:
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
