import speech_recognition as sr

from .speech_transcriber import SpeechTranscriber


class GoogleCloudSpeechTranscriber(SpeechTranscriber):
    def __init__(self, credentials_filepath: str) -> None:
        self._credentials_filepath = credentials_filepath
        self._speech_recognizer = sr.Recognizer()

    def transcribe(self, audio_data: sr.AudioData) -> str:
        return self._speech_recognizer.recognize_google_cloud(
            audio_data, credentials_json=self._credentials_filepath
        )
