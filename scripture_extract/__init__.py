import abc
import os
import tempfile

import openai
import speech_recognition as sr


class SpeechTranscriber(abc.ABC):
    @abc.abstractmethod
    def transcribe(self, audio_data: sr.AudioData) -> str:
        pass


class GoogleCloudSpeechTranscriber(SpeechTranscriber):
    def __init__(self, credentials_filepath: str) -> None:
        self._credentials_filepath = credentials_filepath
        self._speech_recognizer = sr.Recognizer()

    def transcribe(self, audio_data: sr.AudioData) -> str:
        print("[GoogleCloudSpeechTranscriber] Got it! Now to recognize it...")
        return self._speech_recognizer.recognize_google_cloud(audio_data, credentials_json=self._credentials_filepath)


class SphinxSpeechTranscriber(SpeechTranscriber):
    def __init__(self, keywords: list[str] = None) -> None:
        self._speech_recognizer = sr.Recognizer()
        self._keywords = [(kw.lower(), 1)
                          for kw in keywords] if keywords is not None else None

    def transcribe(self, audio_data: sr.AudioData) -> str:
        print("[SphinxSpeechTranscriber] Got it! Now to recognize it...")
        return self._speech_recognizer.recognize_sphinx(audio_data, keyword_entries=self._keywords)


class OpenAIWhisperSpeechTranscriber(SpeechTranscriber):
    def __init__(self, *, prompt: str = "", api_key: str) -> None:
        self._prompt = prompt
        self._api_key = api_key

    def transcribe(self, audio_data: sr.AudioData) -> str:
        print("[OpenAIWhisperSpeechTranscriber] Got it! Now to transcribe it...")
        with tempfile.NamedTemporaryFile(suffix=".wav") as audio_file:
            audio_file.write(audio_data.get_wav_data())
            audio_file.seek(0)
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                prompt=self._prompt,
                api_key=self._api_key,
            )
        return response["text"]


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
