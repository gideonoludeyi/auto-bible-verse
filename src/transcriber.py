import os
import argparse
import sys

import speech_recognition as sr

from autoscript.openai_whisper_speech_transcriber import (
    OpenAIWhisperSpeechTranscriber,
)

parser = argparse.ArgumentParser(
    prog="Speech to Text", description="transcribes a WAV audio file to text"
)
parser.add_argument(
    "-f",
    "--file",
    dest="audiofile",
    help="filepath to the WAV audio file. [default: read from stdin or use `-`]",
    type=argparse.FileType("rb"),
    default=sys.stdin.buffer,
)
parser.add_argument(
    "-c",
    "--credentials",
    dest="credentials",
    help="OpenAI api key",
    type=str,
    default=os.getenv("OPENAI_API_KEY"),
)


def main():
    args = parser.parse_args()

    assert args.credentials is not None

    recognizer = sr.Recognizer()
    with sr.AudioFile(args.audiofile) as source:
        audio_data = recognizer.record(source)

    transcriber = OpenAIWhisperSpeechTranscriber(api_key=args.credentials)

    try:
        text = transcriber.transcribe(audio_data)
        print(text)
    except sr.UnknownValueError as e:
        print(f"Oops! didn't catch that: {e}", file=sys.stderr)
    except sr.RequestError as e:
        print(e, file=sys.stderr)
