import os
import argparse
import sys
import pathlib

import speech_recognition as sr

from scripture_extract.openai_whisper_speech_transcriber import (
    OpenAIWhisperSpeechTranscriber
)

parser = argparse.ArgumentParser(
    prog="Speech to Text", description="transcribes a WAV audio file to text")
parser.add_argument(
    "-f", "--file",
    dest="filepath",
    help="filepath to the WAV audio file. [default: read from stdin]",
    type=pathlib.Path)
parser.add_argument("-c", "--credentials", dest="credentials",
                    help="OpenAI api key", type=str,
                    default=os.getenv("OPENAI_API_KEY"))


def main():
    args = parser.parse_args()

    assert args.credentials is not None

    recognizer = sr.Recognizer()
    if args.filepath is not None:
        with sr.AudioFile(str(args.filepath)) as source:
            audio_data = recognizer.record(source)
    else:
        with sr.AudioFile(sys.stdin.buffer) as source:
            audio_data = recognizer.record(source)

    transcriber = OpenAIWhisperSpeechTranscriber(
        api_key=args.credentials)

    try:
        text = transcriber.transcribe(audio_data)
        print(text)
    except sr.UnknownValueError as e:
        print(f"Oops! didn't catch that: {e}", file=sys.stderr)
    except sr.RequestError as e:
        print(e, file=sys.stderr)
