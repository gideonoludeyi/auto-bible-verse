import abc
import json
import os

import speech_recognition as sr


class SpeechRecognizer(abc.ABC):
    @abc.abstractmethod
    def recognize(self, audio_data: sr.AudioData) -> str:
        pass


class GoogleCloudSpeechRecognizer(SpeechRecognizer):
    def __init__(self, credentials_filepath: str) -> None:
        self._credentials_filepath = credentials_filepath
        self._speech_recognizer = sr.Recognizer()

    def recognize(self, audio_data: sr.AudioData) -> str:
        print("[GoogleCloudSpeechRecognizer] Got it! Now to recognize it...")
        return self._speech_recognizer.recognize_google_cloud(audio_data, credentials_json=self._credentials_filepath)


class SphinxSpeechRecognizer(SpeechRecognizer):
    def __init__(self, keywords: list[str] = None) -> None:
        self._speech_recognizer = sr.Recognizer()
        self._keywords = [(kw.lower(), 1)
                          for kw in keywords] if keywords is not None else None

    def recognize(self, audio_data: sr.AudioData) -> str:
        print("[SphinxSpeechRecognizer] Got it! Now to recognize it...")
        return self._speech_recognizer.recognize_sphinx(audio_data, keyword_entries=self._keywords)


def listen(microphone: sr.Microphone, phrase_time_limit=5, timeout=10):
    recognizer = sr.Recognizer()

    print("A moment of silence...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    print(f"Set minimum energy threshold to {recognizer.energy_threshold}")

    while True:
        with microphone as source:
            print("listening...")
            yield recognizer.listen(source, phrase_time_limit=phrase_time_limit, timeout=timeout)


def main():
    google_credentials_filepath = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS_FILEPATH")
    assert google_credentials_filepath is not None

    with open('data/books.json') as f:
        books = json.load(fp=f)
    recognizer = SphinxSpeechRecognizer(keywords=books)
    microphone = sr.Microphone()

    try:
        for audio_data in listen(microphone):
            try:
                value = recognizer.recognize(audio_data)
                print(f"Speech \"{value}\"")
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print(e)
    except KeyboardInterrupt:
        pass

