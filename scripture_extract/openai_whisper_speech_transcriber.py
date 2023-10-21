import tempfile
import openai
import speech_recognition as sr

from .speech_transcriber import SpeechTranscriber


class OpenAIWhisperSpeechTranscriber(SpeechTranscriber):
    def __init__(self, *, prompt: str = "", api_key: str) -> None:
        self._prompt = prompt
        self._api_key = api_key

    def transcribe(self, audio_data: sr.AudioData) -> str:
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
