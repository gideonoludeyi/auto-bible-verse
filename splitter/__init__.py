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


def clip_filename(start_offset: int, end_offset: int, total_duration: int) -> str:
    ndigits = len(str(int(total_duration)))
    start = str(int(start_offset)).zfill(ndigits)
    end = str(int(end_offset)).zfill(ndigits)
    return f"clip_{start}s-{end}s"


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
            f"{clip_filename(start_offset, end_offset, audio.duration_seconds)}.wav"), format="wav")

        start_offset += segment_duration / 2
        end_offset = start_offset + segment_duration

    new_segment = audio[ms(start_offset):]
    new_segment.export(output_dir.joinpath(
        f"{clip_filename(start_offset, audio.duration_seconds, audio.duration_seconds)}.wav"), format="wav")
