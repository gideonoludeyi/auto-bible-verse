import abc

import speech_recognition as sr


class SpeechTranscriber(abc.ABC):
    @abc.abstractmethod
    def transcribe(self, audio_data: sr.AudioData) -> str:
        pass
