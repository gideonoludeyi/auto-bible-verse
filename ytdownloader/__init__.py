import argparse
import os
import pathlib
import subprocess
from concurrent.futures import ThreadPoolExecutor

import pytube

parser = argparse.ArgumentParser(
    prog="YouTube Downloader", description="downloads a youtube video in WAV format")
parser.add_argument(
    "youtube_urls", help="URL of the youtube video", nargs="+")
parser.add_argument("-o", "--output-dir", dest="output_dir",
                    help="the directory to save the downloaded WAV file", type=pathlib.Path, default="out")
parser.add_argument(
    "-w", "--workers", dest="n_workers", help="number of concurrent threads to use", type=int, default=5)


def download(url: str, out_dir: pathlib.Path) -> None:
    path = (
        pytube.YouTube(url).streams
        .filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
        .download(out_dir)
    )

    filename, _ = os.path.splitext(path)

    subprocess.run(
        ["ffmpeg", "-i", path, f"{filename}.wav", "-y", "-v", "error"])

    os.unlink(path)


def main():
    args = parser.parse_args()

    youtube_urls = set(args.youtube_urls)
    output_dir = args.output_dir
    n_workers = args.n_workers

    if not output_dir.exists():
        os.mkdir(output_dir)

    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        for url in youtube_urls:
            executor.submit(download, url, output_dir)
