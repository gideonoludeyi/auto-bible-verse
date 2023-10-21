import os

import speech_recognition as sr

from .openai_whisper_speech_transcriber import OpenAIWhisperSpeechTranscriber
from .openai_chat_completion_scripture_inferer import (
    OpenAIChatCompletionScriptureInferer
)


def listen(microphone: sr.Microphone, phrase_time_limit=5, timeout=10):
    recognizer = sr.Recognizer()

    print("A moment of silence...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    print(f"Set minimum energy threshold to {recognizer.energy_threshold}")

    while True:
        with microphone as source:
            print("listening...")
            yield recognizer.listen(
                source,
                phrase_time_limit=phrase_time_limit,
                timeout=timeout)


def main():
    transcriber = OpenAIWhisperSpeechTranscriber(
        api_key=os.getenv("OPENAI_API_KEY"))

    scripture_inferer = OpenAIChatCompletionScriptureInferer(
        api_key=os.getenv("OPENAI_API_KEY"))

    microphone = sr.Microphone()

    try:
        for audio_data in listen(microphone):
            value = transcriber.transcribe(audio_data)
            print(f"Speech \"{value}\"")
            print(scripture_inferer.infer(value))
    except KeyboardInterrupt:
        pass
