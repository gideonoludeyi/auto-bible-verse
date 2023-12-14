import sys
import argparse
from typing import BinaryIO

import pytube

parser = argparse.ArgumentParser(
    prog="YouTube Downloader", description="downloads a youtube video in MP4 format"
)
parser.add_argument("youtube_url", help="URL of the youtube video")
parser.add_argument(
    "-o",
    "--output",
    dest="outputfile",
    help="the filepath to save the video. [default: output to stdout or use `-`]",
    type=argparse.FileType("wb"),
    default=sys.stdout.buffer,
)


def download(url: str, buffer: BinaryIO, extension: str) -> None:
    stream = (
        pytube.YouTube(url)
        .streams.filter(progressive=True, file_extension=extension)
        .order_by("resolution")
        .desc()
        .first()
    )
    if stream is not None:
        stream.stream_to_buffer(buffer)


def main():
    args = parser.parse_args()

    youtube_url = args.youtube_url
    outfile = args.outputfile

    with outfile:
        download(youtube_url, outfile, extension="mp4")
