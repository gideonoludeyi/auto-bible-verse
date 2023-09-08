import argparse
import sys
import pathlib

import speech_recognition as sr

parser = argparse.ArgumentParser(prog="Speech to Text", description="transcribes a WAV audio file to text")
parser.add_argument("filepath", help="filepath to the WAV audio file", type=pathlib.Path)
parser.add_argument("-c", "--credentials", dest="credentials", help="filepath to the Google Service Account Credentials JSON", required=True, type=pathlib.Path)

def main():
  args = parser.parse_args()

  audio_filepath = args.filepath
  credentials_filepath = args.credentials

  source = sr.AudioFile(str(audio_filepath))
  recognizer = sr.Recognizer()

  with source:
    audio_data = recognizer.record(source)

  try:
    text = recognizer.recognize_google_cloud(audio_data, credentials_json=str(credentials_filepath))
    print(text)
  except sr.UnknownValueError:
    print("Oops! didn't catch that")
  except sr.RequestError as e:
    print(e, file=sys.stderr)
