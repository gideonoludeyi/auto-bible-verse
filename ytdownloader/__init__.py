import sys
import argparse
import pathlib
from typing import BinaryIO

import pytube

parser = argparse.ArgumentParser(
    prog="YouTube Downloader", description="downloads a youtube video in MP4 format"
)
parser.add_argument("youtube_url", help="URL of the youtube video")
parser.add_argument(
    "-o",
    "--output",
    dest="output_filepath",
    help="the filepath to save the video. [default: output to stdout]",
    type=pathlib.Path,
)


def download(url: str, buffer: BinaryIO, extension: str = "mp4") -> None:
    (
        pytube.YouTube(url)
        .streams.filter(progressive=True, file_extension=extension)
        .order_by("resolution")
        .desc()
        .first()
        .stream_to_buffer(buffer)
    )


def main():
    args = parser.parse_args()

    youtube_url = args.youtube_url
    output_filepath = args.output_filepath

    if output_filepath is None:
        download(youtube_url, sys.stdout.buffer)
    else:
        with open(output_filepath, "wb") as f:
            download(youtube_url, f, extension="mp4")
