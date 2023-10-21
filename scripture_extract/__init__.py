import os

import openai
import speech_recognition as sr

from .openai_whisper_speech_transcriber import OpenAIWhisperSpeechTranscriber


class OpenAIChatCompletionScriptureInferer:
    def __init__(self, *, api_key: str) -> None:
        self._api_key = api_key

    def infer(self, text: str) -> list[str]:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that is displaying the list of scriptures referenced in a preacher's sermon"},
                {"role": "user",
                    "content": "give me a list of the scriptures referenced in the following text: \"let's read genesis 49 verse 11 and ecclesiastes 4 1 to 3\""},
                {"role": "assistant",
                    "content": "- Genesis 49:11\n- Ecclesiastes 4:1-3"},
                {"role": "user", "content": f"Great! give me the list of scriptures referenced in the following text: {text}"}
            ],
            api_key=self._api_key,
        )
        content = response["choices"][0]["message"]["content"]
        return [ref.replace("- ", "") for ref in content.split("\n")]


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
    transcriber = OpenAIWhisperSpeechTranscriber(
        prompt="3 John 1:2-11",
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
