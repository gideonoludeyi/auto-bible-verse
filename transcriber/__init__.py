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
    "filepath", help="filepath to the WAV audio file", type=pathlib.Path)
parser.add_argument("-c", "--credentials", dest="credentials",
                    help="OpenAI api key", required=True, type=str)


def main():
    args = parser.parse_args()

    with sr.AudioFile(str(args.filepath)) as source:
        recognizer = sr.Recognizer()
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
