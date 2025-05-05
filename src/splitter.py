import argparse
import os
import pathlib
import sys
import wave


parser = argparse.ArgumentParser(
    prog="Audio Splitter",
    description="splits a WAV file into overlapping segments in WAV format",
)
parser.add_argument("wav_file", type=argparse.FileType("rb"))
parser.add_argument(
    "-d", "--clip-duration", dest="clip_duration", type=float, default=8.0
)
parser.add_argument(
    "-o", "--output-dir", dest="output_dir", default="out", type=pathlib.Path
)
parser.add_argument(
    "-s",
    "--start",
    dest="start_seconds",
    type=int,
    default=0,
    help="""\
    assumed to be the start of the audio file if not specified
    """,
)
parser.add_argument(
    "-e",
    "--end",
    dest="end_seconds",
    type=int,
    default=None,
    help="""\
    assumed to be the end of the audio file if not specified
    """,
)


def ms(seconds: int) -> int:
    return seconds * 1000


def clipname(start: int, clip_duration: int, audio_duration: int) -> str:
    end = min(start + clip_duration, audio_duration)
    start_fmt = str(start).rjust(len(str(audio_duration)), "0")
    end_fmt = str(end).rjust(len(str(audio_duration)), "0")
    return f"clip_{start_fmt}s-{end_fmt}s.wav"


def main() -> int:
    args = parser.parse_args()

    clip_duration = args.clip_duration
    outdir = args.output_dir

    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    with args.wav_file as f, wave.open(f, "rb") as wav:
        audio_duration = wav.getnframes() / wav.getframerate()
        n_clip_frames = clip_duration * wav.getframerate()
        end_seconds = (
            min(args.end_seconds, audio_duration)
            if args.end_seconds is not None
            else audio_duration
        )
        start = args.start_seconds
        _ = wav.readframes(start * wav.getframerate())  # skip until start
        buf = wav.readframes(int(n_clip_frames // 2))
        while start + clip_duration <= end_seconds and buf:
            buf2 = wav.readframes(int(n_clip_frames // 2))
            if clip := (buf + buf2):
                clippath = outdir.joinpath(
                    clipname(int(start), int(clip_duration), int(end_seconds))
                )
                with wave.open(str(clippath), "wb") as clipwav:
                    clipwav.setparams(
                        # see https://docs.python.org/3/library/wave.html#wave.Wave_write.setparams
                        # (nchannels, sampwidth, framerate, nframes, comptype, compname)
                        (
                            wav.getnchannels(),
                            wav.getsampwidth(),
                            wav.getframerate(),
                            0,  # nframes (value is inferred)
                            wav.getcomptype(),
                            wav.getcompname(),
                        )
                    )
                    clipwav.writeframes(clip)
                start += clip_duration // 2
                buf = buf2

        # write last bit of clip that is not up to the clip duration
        if start + clip_duration // 2 < end_seconds and buf:
            buf2 = wav.readframes(int(n_clip_frames // 2))
            if clip := (buf + buf2):
                clippath = outdir.joinpath(
                    clipname(int(start), int(clip_duration), int(end_seconds))
                )
                with wave.open(str(clippath), "wb") as clipwav:
                    clipwav.setparams(
                        # see https://docs.python.org/3/library/wave.html#wave.Wave_write.setparams
                        # (nchannels, sampwidth, framerate, nframes, comptype, compname)
                        (
                            wav.getnchannels(),
                            wav.getsampwidth(),
                            wav.getframerate(),
                            0,  # nframes (value is inferred)
                            wav.getcomptype(),
                            wav.getcompname(),
                        )
                    )
                    clipwav.writeframes(clip)
    return 0


if __name__ == "__main__":
    sys.exit(main())
