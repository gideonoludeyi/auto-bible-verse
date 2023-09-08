import os
import argparse
import pathlib

import pydub

parser = argparse.ArgumentParser(
    prog="Audio Splitter", description="splits a MP3 file into several overlapping segments in WAV format")
parser.add_argument("filename")
parser.add_argument("-d", "--segment-duration",
                    dest="segment_duration", default="8")
parser.add_argument("-o", "--output-dir", dest="output_dir", default="out")


def ms(seconds: int) -> int:
    return seconds * 1000


def main():
    args = parser.parse_args()

    audio_filename = args.filename
    segment_duration = float(args.segment_duration)
    output_dir = pathlib.Path(args.output_dir)

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    audio = pydub.AudioSegment.from_mp3(audio_filename)

    start_offset = 0
    end_offset = start_offset + segment_duration
    while end_offset < audio.duration_seconds:
        new_segment = audio[ms(start_offset): ms(end_offset)]
        new_segment.export(output_dir.joinpath(
            f"clip_{int(start_offset)}s-{int(end_offset)}s.wav"), format="wav")

        start_offset += segment_duration / 2
        end_offset = start_offset + segment_duration

    new_segment = audio[ms(start_offset):]
    new_segment.export(output_dir.joinpath(
        f"clip_{int(start_offset)}s-{int(audio.duration_seconds)}s.wav"), format="wav")
