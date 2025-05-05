import io
import openai
import speech_recognition as sr

from .speech_transcriber import SpeechTranscriber


class OpenAIWhisperSpeechTranscriber(SpeechTranscriber):
    def __init__(self, *, prompt: str = "", api_key: str) -> None:
        self._prompt = prompt
        self._api_key = api_key

    def transcribe(self, audio_data: sr.AudioData) -> str:
        wav_data = io.BytesIO(audio_data.get_wav_data())
        wav_data.name = "audio.wav"
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=wav_data,
            prompt=self._prompt,
            api_key=self._api_key,
        )
        return response["text"]
