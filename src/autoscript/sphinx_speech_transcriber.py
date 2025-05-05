import speech_recognition as sr

from .speech_transcriber import SpeechTranscriber


class SphinxSpeechTranscriber(SpeechTranscriber):
    def __init__(self, keywords: list[str] | None = None) -> None:
        self._speech_recognizer = sr.Recognizer()
        self._keywords = (
            [(kw.lower(), 1) for kw in keywords] if keywords is not None else None
        )

    def transcribe(self, audio_data: sr.AudioData) -> str:
        return self._speech_recognizer.recognize_sphinx(
            audio_data, keyword_entries=self._keywords
        )
