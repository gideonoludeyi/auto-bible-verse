import os
import argparse
import pathlib

import pydub

parser = argparse.ArgumentParser(
    prog="Audio Splitter", description="splits a MP3 file into several overlapping segments in WAV format")
parser.add_argument("filename")
parser.add_argument("-d", "--segment-duration",
                    dest="segment_duration", type=float, default=8.0)
parser.add_argument("-o", "--output-dir", dest="output_dir",
                    default="out", type=pathlib.Path)
parser.add_argument("-s", "--start", dest="start_seconds",
                    type=float, default=0.0)
parser.add_argument("-e", "--end", dest="end_seconds",
                    type=float, default=float("inf"))


def ms(seconds: int) -> int:
    return seconds * 1000


def clip_filename(start_offset: int, end_offset: int, total_duration: int) -> str:
    ndigits = len(str(int(total_duration)))
    start = str(int(start_offset)).zfill(ndigits)
    end = str(int(end_offset)).zfill(ndigits)
    return f"clip_{start}s-{end}s"


def main():
    args = parser.parse_args()

    audio_filename = args.filename
    segment_duration = args.segment_duration
    output_dir = args.output_dir

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    audio = pydub.AudioSegment.from_mp3(audio_filename)

    start = args.start_seconds
    end = min(args.end_seconds, audio.duration_seconds)

    start_offset = start
    end_offset = start_offset + segment_duration
    while end_offset < end:
        new_segment = audio[ms(start_offset): ms(end_offset)]
        new_segment.export(output_dir.joinpath(
            f"{clip_filename(start_offset, end_offset, end)}.wav"), format="wav")

        start_offset += segment_duration / 2
        end_offset = start_offset + segment_duration

    new_segment = audio[ms(start_offset):]
    new_segment.export(output_dir.joinpath(
        f"{clip_filename(start_offset, end, end)}.wav"), format="wav")
